from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/{project_id}", response_model=schemas.Task, summary="Create a new task", description="Create a task for a specific project, optionally assigning it to a user.")
def create_task(project_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.deleted_at.is_(None)).first()
    if not project or (project.user_id != current_user.id and not (project.group_id and crud.check_group_permission(db, project.group_id, current_user.id, "edit"))):
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        return crud.create_project_task(db=db, task=task, project_id=project_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{project_id}/{task_id}", response_model=schemas.Task, summary="Update a task", description="Update an existing task for a specific project, optionally reassigning it to a user.")
def update_task(project_id: int, task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.deleted_at.is_(None)).first()
    if not project or (project.user_id != current_user.id and not (project.group_id and crud.check_group_permission(db, project.group_id, current_user.id, "edit"))):
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        return crud.update_project_task(db, task_id, project_id, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{project_id}", response_model=List[schemas.Task], summary="List tasks", description="Retrieve tasks for a specific project, if authorized.")
def read_tasks(project_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_tasks(db, project_id=project_id, user_id=current_user.id)

@router.delete("/{project_id}/{task_id}", response_model=dict, summary="Soft delete task", description="Mark a task as deleted without removing it from the database.")
def delete_task(project_id: int, task_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.deleted_at.is_(None)).first()
    if not project or (project.user_id != current_user.id and not (project.group_id and crud.check_group_permission(db, project.group_id, current_user.id, "edit"))):
        raise HTTPException(status_code=403, detail="Not authorized")
    task = crud.soft_delete_task(db, task_id, project_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}