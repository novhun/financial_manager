from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/incomes", tags=["incomes"])

@router.post("/", response_model=schemas.Income, summary="Create a new income", description="Create an income entry for the authenticated user, optionally linked to a group or project.")
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    try:
        return crud.create_user_income(db=db, income=income, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{income_id}", response_model=schemas.Income, summary="Update an income", description="Update an existing income entry for the authenticated user.")
def update_income(income_id: int, income: schemas.IncomeCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_income = db.query(models.Income).filter(models.Income.id == income_id, models.Income.user_id == current_user.id, models.Income.deleted_at.is_(None)).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found or not authorized")
    if income.group_id and not crud.check_group_permission(db, income.group_id, current_user.id, "edit"):
        raise HTTPException(status_code=403, detail="Not authorized for this group")
    try:
        type_obj = crud.get_income_type(db, income.type_id, current_user.id)
        if not type_obj:
            raise ValueError(f"Income type ID '{income.type_id}' does not exist or not authorized")
        if income.project_id:
            project = db.query(models.Project).filter(models.Project.id == income.project_id, models.Project.deleted_at.is_(None)).first()
            if not project or (project.user_id != current_user.id and not (project.group_id and crud.check_group_permission(db, project.group_id, current_user.id, "edit"))):
                raise ValueError(f"Project ID '{income.project_id}' does not exist or not authorized")
        db_income.amount = income.amount
        db_income.type_id = income.type_id
        db_income.description = income.description
        db_income.date = income.date or datetime.utcnow()
        db_income.group_id = income.group_id
        db_income.project_id = income.project_id
        db.commit()
        db.refresh(db_income)
        return db_income
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Income], summary="List incomes", description="Retrieve incomes for the authenticated user or their groups, with optional filtering by type_id, project_id, and date range.")
def read_incomes(
    skip: int = 0,
    limit: int = 100,
    type_id: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    return crud.get_incomes(db, user_id=current_user.id, skip=skip, limit=limit, type_id=type_id, start_date=start_date, end_date=end_date, project_id=project_id)

@router.delete("/{income_id}", response_model=dict, summary="Soft delete income", description="Mark an income as deleted without removing it from the database.")
def delete_income(income_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    income = crud.soft_delete_income(db, income_id, current_user.id)
    if not income:
        raise HTTPException(status_code=404, detail="Income not found or not authorized")
    return {"message": "Income deleted"}