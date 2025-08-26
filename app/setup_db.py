from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, IncomeType, ExpenseType, BudgetCategory, User, Group
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def setup_database():
    Base.metadata.create_all(bind=engine)

    default_income_types = ["salary", "investment", "freelance", "other"]
    default_expense_types = ["food", "rent", "utilities", "entertainment", "other"]
    default_budget_categories = ["food", "rent", "utilities", "entertainment", "other"]
    default_user = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin123"
    }
    default_group = {
        "name": "Family",
        "description": "Default family finance group"
    }

    db = SessionLocal()
    try:
        # Seed default user
        user = db.query(User).filter(User.username == default_user["username"]).first()
        if not user:
            hashed_password = pwd_context.hash(default_user["password"])
            user = User(
                username=default_user["username"],
                email=default_user["email"],
                hashed_password=hashed_password
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Seed default group
        if not db.query(Group).filter(Group.name == default_group["name"]).first():
            group = Group(
                name=default_group["name"],
                description=default_group["description"],
                owner_id=user.id
            )
            db.add(group)
            db.commit()
            db.refresh(group)
            db.execute(models.user_group.insert().values(user_id=user.id, group_id=group.id))
            db.commit()

        # Seed income types
        for name in default_income_types:
            if not db.query(IncomeType).filter(IncomeType.name == name).first():
                db.add(IncomeType(name=name))
        # Seed expense types
        for name in default_expense_types:
            if not db.query(ExpenseType).filter(ExpenseType.name == name).first():
                db.add(ExpenseType(name=name))
        # Seed budget categories
        for name in default_budget_categories:
            if not db.query(BudgetCategory).filter(BudgetCategory.name == name).first():
                db.add(BudgetCategory(name=name))
        db.commit()
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()