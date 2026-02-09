"""Task API routes."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from backend.models.database import get_db
from backend.models.schemas import TaskCreate, TaskResponse, TaskBase
from backend.models.schemas import Task as TaskModel

router = APIRouter()


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """Create a new task."""
    try:
        db_task = TaskModel(
            client_id=task.client_id,
            campaign_id=task.campaign_id,
            agent_type=task.agent_type,
            status="pending",
            input_data=task.input_data
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return TaskResponse.model_validate(db_task)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    client_id: Optional[int] = None,
    campaign_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get tasks with optional filters."""
    try:
        query = db.query(TaskModel)
        
        if client_id:
            query = query.filter(TaskModel.client_id == client_id)
        if campaign_id:
            query = query.filter(TaskModel.campaign_id == campaign_id)
        if status:
            query = query.filter(TaskModel.status == status)
        
        tasks = query.offset(skip).limit(limit).all()
        return [TaskResponse.model_validate(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific task."""
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    status: Optional[str] = None,
    output_data: Optional[dict] = None,
    error_message: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update a task."""
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if status:
            task.status = status
        if output_data is not None:
            task.output_data = output_data
        if error_message:
            task.error_message = error_message
        
        if status == "completed":
            task.completed_at = datetime.utcnow()
        
        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)
        return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Delete a task."""
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
