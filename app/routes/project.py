from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.project import ProjectCRUD
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.database import get_async_session
from app.schemas.task import TaskRead

router = APIRouter()

# Create a new project
@router.post("/", response_model=ProjectRead)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_async_session)):
    return await ProjectCRUD.create_project(db=db, project=project)

# Get project by ID
@router.get("/{project_id}", response_model=ProjectRead)
async def read_project(project_id: int, db: AsyncSession = Depends(get_async_session)):
    return await ProjectCRUD.get_project_by_id(db=db, project_id=project_id)

# Get all tasks by project ID
@router.get("/{project_id}/tasks", response_model=List[TaskRead])
async def read_tasks_by_project(project_id: int, db: AsyncSession = Depends(get_async_session)):
    return await ProjectCRUD.get_tasks_by_project_id(db=db, project_id=project_id)

# Update project
@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: int, project: ProjectUpdate, db: AsyncSession = Depends(get_async_session)):
    return await ProjectCRUD.update_project(db=db, project_id=project_id, project_update=project)

# Delete project
@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_async_session)):
    success = await ProjectCRUD.delete_project(db=db, project_id=project_id)
    return {"deleted": success}
