from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary", response_model=schemas.FinancialSummary, summary="Financial summary", description="Get total income, expense, net balance, and budget status for the user or a specific group.")
def get_financial_summary(
    group_id: int = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    if group_id:
        group = next((g for g in current_user.groups if g.id == group_id and g.deleted_at is None), None)
        if not group:
            raise HTTPException(status_code=403, detail="Not authorized for this group")
    return crud.get_financial_summary(db, user_id=current_user.id, group_id=group_id)