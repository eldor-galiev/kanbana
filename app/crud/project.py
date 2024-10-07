from typing import Any, Sequence

from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Project, Task
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectCRUD:
    # CREATE
    async def create_project(db: AsyncSession, project: ProjectCreate) -> Project:
        new_project = Project(name=project.name, owner_id=project.owner_id)

        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        return new_project


    # READ
    async def get_project_by_id(db: AsyncSession, project_id: int) -> Project:
        result = await db.execute(select(Project).where(Project.id == project_id))
        return result.scalars().first()


    # Get all tasks by project ID
    async def get_tasks_by_project_id(db: AsyncSession, project_id: int) -> Sequence[Task]:
        result = await db.execute(select(Task).where(Task.project_id == project_id))
        return result.scalars().all()


    # UPDATE
    async def update_project(db: AsyncSession, project_id: int, project_update: ProjectUpdate) -> Project:
        result = await db.execute(
            select(Project).where(Project.id == project_id).options(selectinload(Project.tasks))
        )
        project = result.scalars().first()

        if project:
            for key, value in project_update.model_dump(exclude_unset=True).items():
                setattr(project, key, value)
            await db.commit()
            await db.refresh(project)
        return project


    # DELETE
    async def delete_project(db: AsyncSession, project_id: int) -> bool:
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalars().first()

        if project:
            await db.delete(project)
            await db.commit()
            return True
        return False
