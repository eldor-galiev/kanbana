from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud.task import TaskCRUD
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.database import get_async_session

router = APIRouter()

# Create a new task
@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_async_session)):
    return await TaskCRUD.create_task(db=db, task=task)

# Get task by ID
@router.get("/{task_id}", response_model=TaskRead)
async def read_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    return await TaskCRUD.get_task_by_id(db=db, task_id=task_id)

# Update task
@router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_async_session)):
    return await TaskCRUD.update_task(db=db, task_id=task_id, task_update=task)

# Delete task
@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    success = await TaskCRUD.delete_task(db=db, task_id=task_id)
    return {"deleted": success}
