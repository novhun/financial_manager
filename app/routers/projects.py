from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=schemas.Project, summary="Create a new project", description="Create a project for the authenticated user, optionally linked to a group.")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    try:
        return crud.create_user_project(db=db, project=project, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.Project], summary="List projects", description="Retrieve projects for the authenticated user or their groups.")
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_projects(db, user_id=current_user.id, skip=skip, limit=limit)

@router.delete("/{project_id}", response_model=dict, summary="Soft delete project", description="Mark a project as deleted without removing it from the database.")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    project = crud.soft_delete_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
    return {"message": "Project deleted"}