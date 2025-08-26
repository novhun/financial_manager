from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.post("/", response_model=schemas.Budget, summary="Create a new budget", description="Create a budget entry for the authenticated user, optionally linked to a group or project.")
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    try:
        return crud.create_user_budget(db=db, budget=budget, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{budget_id}", response_model=schemas.Budget, summary="Update a budget", description="Update an existing budget entry for the authenticated user.")
def update_budget(budget_id: int, budget: schemas.BudgetCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == current_user.id, models.Budget.deleted_at.is_(None)).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found or not authorized")
    if budget.group_id and not crud.check_group_permission(db, budget.group_id, current_user.id, "edit"):
        raise HTTPException(status_code=403, detail="Not authorized for this group")
    try:
        category_obj = crud.get_budget_category(db, budget.category_id, current_user.id)
        if not category_obj:
            raise ValueError(f"Budget category ID '{budget.category_id}' does not exist or not authorized")
        if budget.project_id:
            project = db.query(models.Project).filter(models.Project.id == budget.project_id, models.Project.deleted_at.is_(None)).first()
            if not project or (project.user_id != current_user.id and not (project.group_id and crud.check_group_permission(db, project.group_id, current_user.id, "edit"))):
                raise ValueError(f"Project ID '{budget.project_id}' does not exist or not authorized")
        db_budget.category_id = budget.category_id
        db_budget.amount = budget.amount
        db_budget.period = budget.period
        db_budget.group_id = budget.group_id
        db_budget.project_id = budget.project_id
        db.commit()
        db.refresh(db_budget)
        return db_budget
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Budget], summary="List budgets", description="Retrieve budgets for the authenticated user or their groups, with optional filtering by project_id.")
def read_budgets(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    return crud.get_budgets(db, user_id=current_user.id, skip=skip, limit=limit, project_id=project_id)

@router.delete("/{budget_id}", response_model=dict, summary="Soft delete budget", description="Mark a budget as deleted without removing it from the database.")
def delete_budget(budget_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    budget = crud.soft_delete_budget(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found or not authorized")
    return {"message": "Budget deleted"}