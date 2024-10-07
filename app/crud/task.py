from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskCRUD:
    # CREATE
    async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
        new_task = Task(
            project_id=task.project_id,
            name=task.name,
            description=task.description,
            status=task.status,
            dead_line=task.dead_line
        )
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task


    # READ
    async def get_task_by_id(db: AsyncSession, task_id: int) -> Task:
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalars().first()


    # UPDATE
    async def update_task(db: AsyncSession, task_id: int, task_update: TaskUpdate) -> Task:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()

        if task:
            for key, value in task_update.model_dump(exclude_unset=True).items():
                setattr(task, key, value)
            await db.commit()
            await db.refresh(task)
        return task


    # DELETE
    async def delete_task(db: AsyncSession, task_id: int) -> bool:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()

        if task:
            await db.delete(task)
            await db.commit()
            return True
        return False
