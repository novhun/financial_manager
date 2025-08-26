from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"[^@]+@[^@]+\.[^@]+")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ResetTokenCreate(BaseModel):
    email: str

class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

class IncomeTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class IncomeTypeCreate(IncomeTypeBase):
    pass

class IncomeTypeUpdate(IncomeTypeBase):
    pass

class IncomeType(IncomeTypeBase):
    id: int
    user_id: Optional[int]

    class Config:
        from_attributes = True

class ExpenseTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class ExpenseTypeCreate(ExpenseTypeBase):
    pass

class ExpenseTypeUpdate(ExpenseTypeBase):
    pass

class ExpenseType(ExpenseTypeBase):
    id: int
    user_id: Optional[int]

    class Config:
        from_attributes = True

class BudgetCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class BudgetCategoryCreate(BudgetCategoryBase):
    pass

class BudgetCategoryUpdate(BudgetCategoryBase):
    pass

class BudgetCategory(BudgetCategoryBase):
    id: int
    user_id: Optional[int]

    class Config:
        from_attributes = True

class IncomeBase(BaseModel):
    amount: float = Field(..., gt=0)
    type_id: int
    description: Optional[str] = Field(None, max_length=200)
    date: Optional[datetime] = None
    group_id: Optional[int] = None
    project_id: Optional[int] = None

class IncomeCreate(IncomeBase):
    pass

class Income(IncomeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0)
    type_id: int
    description: Optional[str] = Field(None, max_length=200)
    date: Optional[datetime] = None
    group_id: Optional[int] = None
    project_id: Optional[int] = None

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    category_id: int
    amount: float = Field(..., gt=0)
    period: str = Field(default="monthly", pattern="^(daily|weekly|monthly|yearly)$")
    group_id: Optional[int] = None
    project_id: Optional[int] = None

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    status: str = Field(default="pending", pattern="^(pending|in_progress|done)$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    file_url: Optional[str] = Field(None, max_length=255)
    user_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image_url: Optional[str] = Field(None, max_length=255)
    group_id: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int
    tasks: List[Task] = []

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    owner_id: int
    members: List[User] = []

    class Config:
        from_attributes = True

class GroupShareBase(BaseModel):
    user_id: int
    permission: str = Field(..., pattern="^(view|edit)$")

class GroupShareCreate(GroupShareBase):
    pass

class GroupShare(GroupShareBase):
    group_id: int

    class Config:
        from_attributes = True

class FinancialSummary(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    budget_status: dict