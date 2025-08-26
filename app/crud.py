from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from . import models, schemas
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id, models.User.deleted_at.is_(None)).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username, models.User.deleted_at.is_(None)).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email, models.User.deleted_at.is_(None)).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def soft_delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        user.deleted_at = datetime.utcnow()
        db.commit()
    return user

def create_reset_token(db: Session, user_id: int):
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)
    db_token = models.ResetToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return token

def get_reset_token(db: Session, token: str):
    return db.query(models.ResetToken).filter(models.ResetToken.token == token, models.ResetToken.expires_at > datetime.utcnow()).first()

def delete_reset_token(db: Session, token: str):
    db_token = get_reset_token(db, token)
    if db_token:
        db.delete(db_token)
        db.commit()

def create_income_type(db: Session, income_type: schemas.IncomeTypeCreate, user_id: Optional[int] = None):
    db_income_type = models.IncomeType(name=income_type.name, user_id=user_id)
    db.add(db_income_type)
    db.commit()
    db.refresh(db_income_type)
    return db_income_type

def update_income_type(db: Session, income_type_id: int, income_type: schemas.IncomeTypeUpdate, user_id: int):
    db_income_type = db.query(models.IncomeType).filter(models.IncomeType.id == income_type_id, models.IncomeType.user_id == user_id, models.IncomeType.deleted_at.is_(None)).first()
    if not db_income_type:
        raise HTTPException(status_code=404, detail="Income type not found or not authorized")
    db_income_type.name = income_type.name
    db.commit()
    db.refresh(db_income_type)
    return db_income_type

def soft_delete_income_type(db: Session, income_type_id: int, user_id: int):
    db_income_type = db.query(models.IncomeType).filter(models.IncomeType.id == income_type_id, models.IncomeType.user_id == user_id, models.IncomeType.deleted_at.is_(None)).first()
    if db_income_type:
        db_income_type.deleted_at = datetime.utcnow()
        db.commit()
    return db_income_type

def get_income_type(db: Session, income_type_id: int, user_id: Optional[int] = None):
    query = db.query(models.IncomeType).filter(models.IncomeType.id == income_type_id, models.IncomeType.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.IncomeType.user_id == user_id) | (models.IncomeType.user_id.is_(None)))
    return query.first()

def get_income_type_by_name(db: Session, name: str, user_id: Optional[int] = None):
    query = db.query(models.IncomeType).filter(models.IncomeType.name == name, models.IncomeType.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.IncomeType.user_id == user_id) | (models.IncomeType.user_id.is_(None)))
    return query.first()

def get_income_types(db: Session, user_id: Optional[int] = None):
    query = db.query(models.IncomeType).filter(models.IncomeType.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.IncomeType.user_id == user_id) | (models.IncomeType.user_id.is_(None)))
    return query.all()

def create_expense_type(db: Session, expense_type: schemas.ExpenseTypeCreate, user_id: Optional[int] = None):
    db_expense_type = models.ExpenseType(name=expense_type.name, user_id=user_id)
    db.add(db_expense_type)
    db.commit()
    db.refresh(db_expense_type)
    return db_expense_type

def update_expense_type(db: Session, expense_type_id: int, expense_type: schemas.ExpenseTypeUpdate, user_id: int):
    db_expense_type = db.query(models.ExpenseType).filter(models.ExpenseType.id == expense_type_id, models.ExpenseType.user_id == user_id, models.ExpenseType.deleted_at.is_(None)).first()
    if not db_expense_type:
        raise HTTPException(status_code=404, detail="Expense type not found or not authorized")
    db_expense_type.name = expense_type.name
    db.commit()
    db.refresh(db_expense_type)
    return db_expense_type

def soft_delete_expense_type(db: Session, expense_type_id: int, user_id: int):
    db_expense_type = db.query(models.ExpenseType).filter(models.ExpenseType.id == expense_type_id, models.ExpenseType.user_id == user_id, models.ExpenseType.deleted_at.is_(None)).first()
    if db_expense_type:
        db_expense_type.deleted_at = datetime.utcnow()
        db.commit()
    return db_expense_type

def get_expense_type(db: Session, expense_type_id: int, user_id: Optional[int] = None):
    query = db.query(models.ExpenseType).filter(models.ExpenseType.id == expense_type_id, models.ExpenseType.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.ExpenseType.user_id == user_id) | (models.ExpenseType.user_id.is_(None)))
    return query.first()

def get_expense_type_by_name(db: Session, name: str, user_id: Optional[int] = None):
    query = db.query(models.ExpenseType).filter(models.ExpenseType.name == name, models.ExpenseType.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.ExpenseType.user_id == user_id) | (models.Expensetype.user_id.is_(None)))
    return query.first()

def get_expense_types(db: Session, user_id: Optional[int] = None):
    query = db.query(models.ExpenseType).filter(models.ExpenseType.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.ExpenseType.user_id == user_id) | (models.ExpenseType.user_id.is_(None)))
    return query.all()

def create_budget_category(db: Session, budget_category: schemas.BudgetCategoryCreate, user_id: Optional[int] = None):
    db_budget_category = models.BudgetCategory(name=budget_category.name, user_id=user_id)
    db.add(db_budget_category)
    db.commit()
    db.refresh(db_budget_category)
    return db_budget_category

def update_budget_category(db: Session, budget_category_id: int, budget_category: schemas.BudgetCategoryUpdate, user_id: int):
    db_budget_category = db.query(models.BudgetCategory).filter(models.BudgetCategory.id == budget_category_id, models.BudgetCategory.user_id == user_id, models.BudgetCategory.deleted_at.is_(None)).first()
    if not db_budget_category:
        raise HTTPException(status_code=404, detail="Budget category not found or not authorized")
    db_budget_category.name = budget_category.name
    db.commit()
    db.refresh(db_budget_category)
    return db_budget_category

def soft_delete_budget_category(db: Session, budget_category_id: int, user_id: int):
    db_budget_category = db.query(models.BudgetCategory).filter(models.BudgetCategory.id == budget_category_id, models.BudgetCategory.user_id == user_id, models.BudgetCategory.deleted_at.is_(None)).first()
    if db_budget_category:
        db_budget_category.deleted_at = datetime.utcnow()
        db.commit()
    return db_budget_category

def get_budget_category(db: Session, budget_category_id: int, user_id: Optional[int] = None):
    query = db.query(models.BudgetCategory).filter(models.BudgetCategory.id == budget_category_id, models.BudgetCategory.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.BudgetCategory.user_id == user_id) | (models.BudgetCategory.user_id.is_(None)))
    return query.first()

def get_budget_category_by_name(db: Session, name: str, user_id: Optional[int] = None):
    query = db.query(models.BudgetCategory).filter(models.BudgetCategory.name == name, models.BudgetCategory.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.BudgetCategory.user_id == user_id) | (models.BudgetCategory.user_id.is_(None)))
    return query.first()

def get_budget_categories(db: Session, user_id: Optional[int] = None):
    query = db.query(models.BudgetCategory).filter(models.BudgetCategory.deleted_at.is_(None))
    if user_id:
        query = query.filter((models.BudgetCategory.user_id == user_id) | (models.BudgetCategory.user_id.is_(None)))
    return query.all()

def check_group_permission(db: Session, group_id: int, user_id: int, required_permission: str = "view") -> bool:
    group = db.query(models.Group).filter(models.Group.id == group_id, models.Group.deleted_at.is_(None)).first()
    if not group:
        return False
    if group.owner_id == user_id:
        return True
    share = db.query(models.group_shares).filter(models.group_shares.c.group_id == group_id, models.group_shares.c.user_id == user_id).first()
    if share:
        return share.permission == "edit" or (required_permission == "view" and share.permission == "view")
    user_in_group = db.query(models.user_group).filter(models.user_group.c.group_id == group_id, models.user_group.c.user_id == user_id).first()
    return bool(user_in_group)  # Group members have edit access by default

def create_user_income(db: Session, income: schemas.IncomeCreate, user_id: int):
    type_obj = get_income_type(db, income.type_id, user_id)
    if not type_obj:
        raise ValueError(f"Income type ID '{income.type_id}' does not exist or not authorized")
    if income.group_id and not check_group_permission(db, income.group_id, user_id, "edit"):
        raise ValueError(f"Not authorized to add income to group ID '{income.group_id}'")
    if income.project_id:
        project = db.query(models.Project).filter(models.Project.id == income.project_id, models.Project.deleted_at.is_(None)).first()
        if not project or (project.user_id != user_id and not (project.group_id and check_group_permission(db, project.group_id, user_id, "edit"))):
            raise ValueError(f"Project ID '{income.project_id}' does not exist or not authorized")
    db_income = models.Income(
        amount=income.amount,
        type_id=income.type_id,
        description=income.description,
        date=income.date,
        group_id=income.group_id,
        project_id=income.project_id,
        user_id=user_id
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

def get_incomes(db: Session, user_id: int, skip: int = 0, limit: int = 100, type_id: int = None, start_date: datetime = None, end_date: datetime = None, project_id: int = None):
    query = db.query(models.Income).filter(models.Income.user_id == user_id, models.Income.deleted_at.is_(None))
    if type_id:
        query = query.filter(models.Income.type_id == type_id)
    if start_date:
        query = query.filter(models.Income.date >= start_date)
    if end_date:
        query = query.filter(models.Income.date <= end_date)
    if project_id:
        query = query.filter(models.Income.project_id == project_id)
    incomes = query.offset(skip).limit(limit).all()
    for group in db.query(models.user_group).filter(models.user_group.c.user_id == user_id).all():
        if check_group_permission(db, group.group_id, user_id, "view"):
            group_incomes = db.query(models.Income).filter(models.Income.group_id == group.group_id, models.Income.deleted_at.is_(None))
            if project_id:
                group_incomes = group_incomes.filter(models.Income.project_id == project_id)
            incomes += [i for i in group_incomes.all() if i.user_id != user_id]
    return incomes

def soft_delete_income(db: Session, income_id: int, user_id: int):
    income = db.query(models.Income).filter(models.Income.id == income_id, models.Income.user_id == user_id, models.Income.deleted_at.is_(None)).first()
    if income and income.group_id and not check_group_permission(db, income.group_id, user_id, "edit"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this income")
    if income:
        income.deleted_at = datetime.utcnow()
        db.commit()
    return income

def create_user_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    type_obj = get_expense_type(db, expense.type_id, user_id)
    if not type_obj:
        raise ValueError(f"Expense type ID '{expense.type_id}' does not exist or not authorized")
    if expense.group_id and not check_group_permission(db, expense.group_id, user_id, "edit"):
        raise ValueError(f"Not authorized to add expense to group ID '{expense.group_id}'")
    if expense.project_id:
        project = db.query(models.Project).filter(models.Project.id == expense.project_id, models.Project.deleted_at.is_(None)).first()
        if not project or (project.user_id != user_id and not (project.group_id and check_group_permission(db, project.group_id, user_id, "edit"))):
            raise ValueError(f"Project ID '{expense.project_id}' does not exist or not authorized")
    db_expense = models.Expense(
        amount=expense.amount,
        type_id=expense.type_id,
        description=expense.description,
        date=expense.date,
        group_id=expense.group_id,
        project_id=expense.project_id,
        user_id=user_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 100, type_id: int = None, start_date: datetime = None, end_date: datetime = None, project_id: int = None):
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id, models.Expense.deleted_at.is_(None))
    if type_id:
        query = query.filter(models.Expense.type_id == type_id)
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)
    if project_id:
        query = query.filter(models.Expense.project_id == project_id)
    expenses = query.offset(skip).limit(limit).all()
    for group in db.query(models.user_group).filter(models.user_group.c.user_id == user_id).all():
        if check_group_permission(db, group.group_id, user_id, "view"):
            group_expenses = db.query(models.Expense).filter(models.Expense.group_id == group.group_id, models.Expense.deleted_at.is_(None))
            if project_id:
                group_expenses = group_expenses.filter(models.Expense.project_id == project_id)
            expenses += [e for e in group_expenses.all() if e.user_id != user_id]
    return expenses

def soft_delete_expense(db: Session, expense_id: int, user_id: int):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id, models.Expense.deleted_at.is_(None)).first()
    if expense and expense.group_id and not check_group_permission(db, expense.group_id, user_id, "edit"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this expense")
    if expense:
        expense.deleted_at = datetime.utcnow()
        db.commit()
    return expense

def create_user_budget(db: Session, budget: schemas.BudgetCreate, user_id: int):
    category_obj = get_budget_category(db, budget.category_id, user_id)
    if not category_obj:
        raise ValueError(f"Budget category ID '{budget.category_id}' does not exist or not authorized")
    if budget.group_id and not check_group_permission(db, budget.group_id, user_id, "edit"):
        raise ValueError(f"Not authorized to add budget to group ID '{budget.group_id}'")
    if budget.project_id:
        project = db.query(models.Project).filter(models.Project.id == budget.project_id, models.Project.deleted_at.is_(None)).first()
        if not project or (project.user_id != user_id and not (project.group_id and check_group_permission(db, project.group_id, user_id, "edit"))):
            raise ValueError(f"Project ID '{budget.project_id}' does not exist or not authorized")
    db_budget = models.Budget(
        category_id=budget.category_id,
        amount=budget.amount,
        period=budget.period,
        group_id=budget.group_id,
        project_id=budget.project_id,
        user_id=user_id
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budgets(db: Session, user_id: int, skip: int = 0, limit: int = 100, project_id: int = None):
    query = db.query(models.Budget).filter(models.Budget.user_id == user_id, models.Budget.deleted_at.is_(None))
    if project_id:
        query = query.filter(models.Budget.project_id == project_id)
    budgets = query.offset(skip).limit(limit).all()
    for group in db.query(models.user_group).filter(models.user_group.c.user_id == user_id).all():
        if check_group_permission(db, group.group_id, user_id, "view"):
            group_budgets = db.query(models.Budget).filter(models.Budget.group_id == group.group_id, models.Budget.deleted_at.is_(None))
            if project_id:
                group_budgets = group_budgets.filter(models.Budget.project_id == project_id)
            budgets += [b for b in group_budgets.all() if b.user_id != user_id]
    return budgets

def soft_delete_budget(db: Session, budget_id: int, user_id: int):
    budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user_id, models.Budget.deleted_at.is_(None)).first()
    if budget and budget.group_id and not check_group_permission(db, budget.group_id, user_id, "edit"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this budget")
    if budget:
        budget.deleted_at = datetime.utcnow()
        db.commit()
    return budget

def create_user_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    if project.group_id and not check_group_permission(db, project.group_id, user_id, "edit"):
        raise ValueError(f"Not authorized to add project to group ID '{project.group_id}'")
    db_project = models.Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        image_url=project.image_url,
        user_id=user_id,
        group_id=project.group_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    query = db.query(models.Project).filter(models.Project.user_id == user_id, models.Project.deleted_at.is_(None))
    projects = query.offset(skip).limit(limit).all()
    for group in db.query(models.user_group).filter(models.user_group.c.user_id == user_id).all():
        if check_group_permission(db, group.group_id, user_id, "view"):
            group_projects = db.query(models.Project).filter(models.Project.group_id == group.group_id, models.Project.deleted_at.is_(None))
            projects += [p for p in group_projects.all() if p.user_id != user_id]
    return projects

def soft_delete_project(db: Session, project_id: int, user_id: int):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.user_id == user_id, models.Project.deleted_at.is_(None)).first()
    if project and project.group_id and not check_group_permission(db, project.group_id, user_id, "edit"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    if project:
        project.deleted_at = datetime.utcnow()
        db.commit()
    return project

def create_project_task(db: Session, task: schemas.TaskCreate, project_id: int):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.deleted_at.is_(None)).first()
    if not project:
        raise ValueError(f"Project ID '{project_id}' does not exist")
    if task.user_id:
        user = db.query(models.User).filter(models.User.id == task.user_id, models.User.deleted_at.is_(None)).first()
        if not user:
            raise ValueError(f"User ID '{task.user_id}' does not exist")
        if project.group_id and not check_group_permission(db, project.group_id, task.user_id, "view"):
            raise ValueError(f"User ID '{task.user_id}' is not in the project group")
    db_task = models.Task(
        name=task.name,
        status=task.status,
        start_date=task.start_date,
        end_date=task.end_date,
        file_url=task.file_url,
        project_id=project_id,
        user_id=task.user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_project_task(db: Session, task_id: int, project_id: int, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.project_id == project_id, models.Task.deleted_at.is_(None)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.deleted_at.is_(None)).first()
    if task.user_id:
        user = db.query(models.User).filter(models.User.id == task.user_id, models.User.deleted_at.is_(None)).first()
        if not user:
            raise ValueError(f"User ID '{task.user_id}' does not exist")
        if project.group_id and not check_group_permission(db, project.group_id, task.user_id, "view"):
            raise ValueError(f"User ID '{task.user_id}' is not in the project group")
    db_task.name = task.name
    db_task.status = task.status
    db_task.start_date = task.start_date
    db_task.end_date = task.end_date
    db_task.file_url = task.file_url
    db_task.user_id = task.user_id
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, project_id: int, user_id: int):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.deleted_at.is_(None)).first()
    if not project or (project.user_id != user_id and not (project.group_id and check_group_permission(db, project.group_id, user_id, "view"))):
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(models.Task).filter(models.Task.project_id == project_id, models.Task.deleted_at.is_(None)).all()

def soft_delete_task(db: Session, task_id: int, project_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.project_id == project_id, models.Task.deleted_at.is_(None)).first()
    if task:
        task.deleted_at = datetime.utcnow()
        db.commit()
    return task

def create_group(db: Session, group: schemas.GroupCreate, owner_id: int):
    db_group = models.Group(name=group.name, description=group.description, owner_id=owner_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    # Add owner as a member
    db.execute(models.user_group.insert().values(user_id=owner_id, group_id=db_group.id))
    db.commit()
    return db_group

def add_user_to_group(db: Session, group_id: int, user_id: int):
    group = db.query(models.Group).filter(models.Group.id == group_id, models.Group.deleted_at.is_(None)).first()
    user = get_user(db, user_id)
    if group and user:
        db.execute(models.user_group.insert().values(user_id=user_id, group_id=group_id))
        db.commit()
        return True
    return False

def get_groups_for_user(db: Session, user_id: int):
    return db.query(models.Group).join(models.user_group).filter(models.user_group.c.user_id == user_id, models.Group.deleted_at.is_(None)).all()

def soft_delete_group(db: Session, group_id: int, user_id: int):
    group = db.query(models.Group).filter(models.Group.id == group_id, models.Group.owner_id == user_id, models.Group.deleted_at.is_(None)).first()
    if not group:
        raise HTTPException(status_code=403, detail="Not authorized or group not found")
    group.deleted_at = datetime.utcnow()
    db.commit()
    return group

def create_group_share(db: Session, group_id: int, share: schemas.GroupShareCreate, owner_id: int):
    group = db.query(models.Group).filter(models.Group.id == group_id, models.Group.owner_id == owner_id, models.Group.deleted_at.is_(None)).first()
    if not group:
        raise HTTPException(status_code=403, detail="Not authorized or group not found")
    user = db.query(models.User).filter(models.User.id == share.user_id, models.User.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if share.user_id == owner_id:
        raise HTTPException(status_code=400, detail="Cannot share with group owner")
    db.execute(models.group_shares.insert().values(group_id=group_id, user_id=share.user_id, permission=share.permission))
    db.commit()
    return {"group_id": group_id, "user_id": share.user_id, "permission": share.permission}

def get_group_shares(db: Session, group_id: int, owner_id: int) -> List[schemas.GroupShare]:
    group = db.query(models.Group).filter(models.Group.id == group_id, models.Group.owner_id == owner_id, models.Group.deleted_at.is_(None)).first()
    if not group:
        raise HTTPException(status_code=403, detail="Not authorized or group not found")
    shares = db.query(models.group_shares).filter(models.group_shares.c.group_id == group_id).all()
    return [schemas.GroupShare(group_id=share.group_id, user_id=share.user_id, permission=share.permission) for share in shares]

def delete_group_share(db: Session, group_id: int, user_id: int, owner_id: int):
    group = db.query(models.Group).filter(models.Group.id == group_id, models.Group.owner_id == owner_id, models.Group.deleted_at.is_(None)).first()
    if not group:
        raise HTTPException(status_code=403, detail="Not authorized or group not found")
    share = db.query(models.group_shares).filter(models.group_shares.c.group_id == group_id, models.group_shares.c.user_id == user_id).first()
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")
    db.execute(models.group_shares.delete().where(models.group_shares.c.group_id == group_id, models.group_shares.c.user_id == user_id))
    db.commit()
    return {"message": "Share deleted"}

def get_financial_summary(db: Session, user_id: int, group_id: Optional[int] = None, project_id: Optional[int] = None):
    if group_id and not check_group_permission(db, group_id, user_id, "view"):
        raise HTTPException(status_code=403, detail="Not authorized for this group")
    query = db.query(func.sum(models.Income.amount)).filter(models.Income.user_id == user_id, models.Income.deleted_at.is_(None))
    if project_id:
        query = query.filter(models.Income.project_id == project_id)
    total_income = query.scalar() or 0

    query = db.query(func.sum(models.Expense.amount)).filter(models.Expense.user_id == user_id, models.Expense.deleted_at.is_(None))
    if project_id:
        query = query.filter(models.Expense.project_id == project_id)
    total_expense = query.scalar() or 0

    if group_id:
        group = db.query(models.Group).filter(models.Group.id == group_id, models.Group.deleted_at.is_(None)).first()
        if group:
            group_income_query = db.query(func.sum(models.Income.amount)).filter(models.Income.group_id == group_id, models.Income.deleted_at.is_(None))
            if project_id:
                group_income_query = group_income_query.filter(models.Income.project_id == project_id)
            total_income += group_income_query.scalar() or 0

            group_expense_query = db.query(func.sum(models.Expense.amount)).filter(models.Expense.group_id == group_id, models.Expense.deleted_at.is_(None))
            if project_id:
                group_expense_query = group_expense_query.filter(models.Expense.project_id == project_id)
            total_expense += group_expense_query.scalar() or 0

    budgets = db.query(models.Budget).filter(models.Budget.user_id == user_id, models.Budget.deleted_at.is_(None))
    if project_id:
        budgets = budgets.filter(models.Budget.project_id == project_id)
    budgets = budgets.all()

    budget_status = {}
    for b in budgets:
        category = db.query(models.BudgetCategory).filter(models.BudgetCategory.id == b.category_id).first()
        budget_status[category.name if category else "Unknown"] = {"allocated": b.amount, "spent": 0}

    expenses = db.query(models.Expense).filter(models.Expense.user_id == user_id, models.Expense.deleted_at.is_(None))
    if project_id:
        expenses = expenses.filter(models.Expense.project_id == project_id)
    for expense in expenses.all():
        expense_type = db.query(models.ExpenseType).filter(models.ExpenseType.id == expense.type_id).first()
        if expense_type and expense_type.name in budget_status:
            budget_status[expense_type.name]["spent"] += expense.amount

    return schemas.FinancialSummary(
        total_income=total_income,
        total_expense=total_expense,
        net_balance=total_income - total_expense,
        budget_status=budget_status
    )