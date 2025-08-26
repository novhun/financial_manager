from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=schemas.Group, summary="Create a new group", description="Create a group for the authenticated user, who becomes the owner.")
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.create_group(db=db, group=group, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.Group], summary="List groups", description="Retrieve groups for the authenticated user.")
def read_groups(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_groups_for_user(db, user_id=current_user.id)

@router.delete("/{group_id}", response_model=dict, summary="Soft delete group", description="Mark a group as deleted without removing it from the database, if owned by the user.")
def delete_group(group_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    group = crud.soft_delete_group(db, group_id, current_user.id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found or not authorized")
    return {"message": "Group deleted"}

@router.post("/{group_id}/members/{user_id}", response_model=dict, summary="Add user to group", description="Add a user to a group, if authorized.")
def add_user_to_group(group_id: int, user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    group = db.query(models.Group).filter(models.Group.id == group_id, models.Group.owner_id == current_user.id, models.Group.deleted_at.is_(None)).first()
    if not group:
        raise HTTPException(status_code=403, detail="Not authorized or group not found")
    if crud.add_user_to_group(db, group_id, user_id):
        return {"message": "User added to group"}
    raise HTTPException(status_code=400, detail="Failed to add user to group")

@router.post("/{group_id}/shares", response_model=schemas.GroupShare, summary="Share group with user", description="Share group data with a user, specifying view or edit permissions.")
def create_group_share(group_id: int, share: schemas.GroupShareCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    try:
        result = crud.create_group_share(db, group_id, share, current_user.id)
        return schemas.GroupShare(group_id=result["group_id"], user_id=result["user_id"], permission=result["permission"])
    except HTTPException as e:
        raise e

@router.get("/{group_id}/shares", response_model=List[schemas.GroupShare], summary="List group shares", description="Retrieve all shares for a group, if owned by the user.")
def read_group_shares(group_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_group_shares(db, group_id, current_user.id)

@router.delete("/{group_id}/shares/{user_id}", response_model=dict, summary="Delete group share", description="Remove a user's access to a group, if owned by the user.")
def delete_group_share(group_id: int, user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.delete_group_share(db, group_id, user_id, current_user.id)