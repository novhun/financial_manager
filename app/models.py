from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

user_group = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

group_shares = Table('group_shares', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('permission', String(20), default="view")  # 'view' or 'edit'
)

class IncomeType(Base):
    __tablename__ = "income_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    incomes = relationship("Income", back_populates="type")
    owner = relationship("User")

class ExpenseType(Base):
    __tablename__ = "expense_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    expenses = relationship("Expense", back_populates="type")
    owner = relationship("User")

class BudgetCategory(Base):
    __tablename__ = "budget_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    budgets = relationship("Budget", back_populates="category")
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    deleted_at = Column(DateTime, nullable=True)

    incomes = relationship("Income", back_populates="owner")
    expenses = relationship("Expense", back_populates="owner")
    budgets = relationship("Budget", back_populates="owner")
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="assignee")
    groups = relationship("Group", secondary=user_group, back_populates="members")
    owned_groups = relationship("Group", back_populates="owner")
    income_types = relationship("IncomeType", back_populates="owner")
    expense_types = relationship("ExpenseType", back_populates="owner")
    budget_categories = relationship("BudgetCategory", back_populates="owner")

class ResetToken(Base):
    __tablename__ = "reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String(36), unique=True)
    expires_at = Column(DateTime)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(200), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="owned_groups")
    members = relationship("User", secondary=user_group, back_populates="groups")
    incomes = relationship("Income", back_populates="group")
    expenses = relationship("Expense", back_populates="group")
    budgets = relationship("Budget", back_populates="group")
    projects = relationship("Project", back_populates="group")

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type_id = Column(Integer, ForeignKey("income_types.id"))
    description = Column(String(200), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="incomes")
    group = relationship("Group", back_populates="incomes")
    type = relationship("IncomeType", back_populates="incomes")
    project = relationship("Project", back_populates="incomes")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type_id = Column(Integer, ForeignKey("expense_types.id"))
    description = Column(String(200), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="expenses")
    group = relationship("Group", back_populates="expenses")
    type = relationship("ExpenseType", back_populates="expenses")
    project = relationship("Project", back_populates="expenses")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("budget_categories.id"))
    amount = Column(Float)
    period = Column(String(20), default="monthly")
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="budgets")
    group = relationship("Group", back_populates="budgets")
    category = relationship("BudgetCategory", back_populates="budgets")
    project = relationship("Project", back_populates="budgets")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(500), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    image_url = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="projects")
    group = relationship("Group", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    incomes = relationship("Income", back_populates="project")
    expenses = relationship("Expense", back_populates="project")
    budgets = relationship("Budget", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    status = Column(String(20), default="pending")
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    file_url = Column(String(255), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")