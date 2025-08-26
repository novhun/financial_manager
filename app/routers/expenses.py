from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=schemas.Expense, summary="Create a new expense", description="Create an expense entry for the authenticated user, optionally linked to a group or project.")
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    try:
        return crud.create_user_expense(db=db, expense=expense, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{expense_id}", response_model=schemas.Expense, summary="Update an expense", description="Update an existing expense entry for the authenticated user.")
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == current_user.id, models.Expense.deleted_at.is_(None)).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found or not authorized")
    if expense.group_id and not crud.check_group_permission(db, expense.group_id, current_user.id, "edit"):
        raise HTTPException(status_code=403, detail="Not authorized for this group")
    try:
        type_obj = crud.get_expense_type(db, expense.type_id, current_user.id)
        if not type_obj:
            raise ValueError(f"Expense type ID '{expense.type_id}' does not exist or not authorized")
        if expense.project_id:
            project = db.query(models.Project).filter(models.Project.id == expense.project_id, models.Project.deleted_at.is_(None)).first()
            if not project or (project.user_id != current_user.id and not (project.group_id and crud.check_group_permission(db, project.group_id, current_user.id, "edit"))):
                raise ValueError(f"Project ID '{expense.project_id}' does not exist or not authorized")
        db_expense.amount = expense.amount
        db_expense.type_id = expense.type_id
        db_expense.description = expense.description
        db_expense.date = expense.date or datetime.utcnow()
        db_expense.group_id = expense.group_id
        db_expense.project_id = expense.project_id
        db.commit()
        db.refresh(db_expense)
        return db_expense
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Expense], summary="List expenses", description="Retrieve expenses for the authenticated user or their groups, with optional filtering by type_id, project_id, and date range.")
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    type_id: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    return crud.get_expenses(db, user_id=current_user.id, skip=skip, limit=limit, type_id=type_id, start_date=start_date, end_date=end_date, project_id=project_id)

@router.delete("/{expense_id}", response_model=dict, summary="Soft delete expense", description="Mark an expense as deleted without removing it from the database.")
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    expense = crud.soft_delete_expense(db, expense_id, current_user.id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found or not authorized")
    return {"message": "Expense deleted"}