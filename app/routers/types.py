from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/types", tags=["types"])

@router.post("/income", response_model=schemas.IncomeType, summary="Create a new income type", description="Create a custom income type for the authenticated user.")
def create_income_type(income_type: schemas.IncomeTypeCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    existing_type = crud.get_income_type_by_name(db, income_type.name, current_user.id)
    if existing_type:
        raise HTTPException(status_code=400, detail="Income type already exists")
    return crud.create_income_type(db, income_type, current_user.id)

@router.put("/income/{income_type_id}", response_model=schemas.IncomeType, summary="Update an income type", description="Update a custom income type owned by the authenticated user.")
def update_income_type(income_type_id: int, income_type: schemas.IncomeTypeUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    updated_type = crud.update_income_type(db, income_type_id, income_type, current_user.id)
    if not updated_type:
        raise HTTPException(status_code=404, detail="Income type not found or not authorized")
    return updated_type

@router.delete("/income/{income_type_id}", response_model=dict, summary="Soft delete an income type", description="Soft delete a custom income type owned by the authenticated user.")
def delete_income_type(income_type_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    income_type = crud.soft_delete_income_type(db, income_type_id, current_user.id)
    if not income_type:
        raise HTTPException(status_code=404, detail="Income type not found or not authorized")
    return {"message": "Income type deleted"}

@router.get("/income", response_model=List[schemas.IncomeType], summary="List income types", description="Retrieve all income types available to the authenticated user, including default and custom types.")
def read_income_types(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_income_types(db, current_user.id)

@router.post("/expense", response_model=schemas.ExpenseType, summary="Create a new expense type", description="Create a custom expense type for the authenticated user.")
def create_expense_type(expense_type: schemas.ExpenseTypeCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    existing_type = crud.get_expense_type_by_name(db, expense_type.name, current_user.id)
    if existing_type:
        raise HTTPException(status_code=400, detail="Expense type already exists")
    return crud.create_expense_type(db, expense_type, current_user.id)

@router.put("/expense/{expense_type_id}", response_model=schemas.ExpenseType, summary="Update an expense type", description="Update a custom expense type owned by the authenticated user.")
def update_expense_type(expense_type_id: int, expense_type: schemas.ExpenseTypeUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    updated_type = crud.update_expense_type(db, expense_type_id, expense_type, current_user.id)
    if not updated_type:
        raise HTTPException(status_code=404, detail="Expense type not found or not authorized")
    return updated_type

@router.delete("/expense/{expense_type_id}", response_model=dict, summary="Soft delete an expense type", description="Soft delete a custom expense type owned by the authenticated user.")
def delete_expense_type(expense_type_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    expense_type = crud.soft_delete_expense_type(db, expense_type_id, current_user.id)
    if not expense_type:
        raise HTTPException(status_code=404, detail="Expense type not found or not authorized")
    return {"message": "Expense type deleted"}

@router.get("/expense", response_model=List[schemas.ExpenseType], summary="List expense types", description="Retrieve all expense types available to the authenticated user, including default and custom types.")
def read_expense_types(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_expense_types(db, current_user.id)

@router.post("/budget", response_model=schemas.BudgetCategory, summary="Create a new budget category", description="Create a custom budget category for the authenticated user.")
def create_budget_category(budget_category: schemas.BudgetCategoryCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    existing_category = crud.get_budget_category_by_name(db, budget_category.name, current_user.id)
    if existing_category:
        raise HTTPException(status_code=400, detail="Budget category already exists")
    return crud.create_budget_category(db, budget_category, current_user.id)

@router.put("/budget/{budget_category_id}", response_model=schemas.BudgetCategory, summary="Update a budget category", description="Update a custom budget category owned by the authenticated user.")
def update_budget_category(budget_category_id: int, budget_category: schemas.BudgetCategoryUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    updated_category = crud.update_budget_category(db, budget_category_id, budget_category, current_user.id)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Budget category not found or not authorized")
    return updated_category

@router.delete("/budget/{budget_category_id}", response_model=dict, summary="Soft delete a budget category", description="Soft delete a custom budget category owned by the authenticated user.")
def delete_budget_category(budget_category_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    budget_category = crud.soft_delete_budget_category(db, budget_category_id, current_user.id)
    if not budget_category:
        raise HTTPException(status_code=404, detail="Budget category not found or not authorized")
    return {"message": "Budget category deleted"}

@router.get("/budget", response_model=List[schemas.BudgetCategory], summary="List budget categories", description="Retrieve all budget categories available to the authenticated user, including default and custom categories.")
def read_budget_categories(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_budget_categories(db, current_user.id)