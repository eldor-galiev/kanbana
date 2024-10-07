from typing import Sequence, Any
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import User, Project
from app.schemas.user import UserUpdate, UserCreate  # Объявления Pydantic схем для создания и обновления


class UserCRUD:
    # CREATE
    async def create_user(db: AsyncSession, user: UserCreate) -> User:
        new_user = User(name=user.name, email=user.email)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    # READ
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
        result = await db.execute(
            select(User).where(User.id == user_id).options(selectinload(User.projects))
        )
        return result.scalars().first()

    async def get_projects_by_user_id(db: AsyncSession, user_id: int) -> Sequence[Project]:
        result = await db.execute(
            select(Project).where(Project.owner_id == user_id).options(selectinload(Project.owner))
        )
        return result.scalars().all()

    # UPDATE
    async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
        result = await db.execute(
            select(User).where(User.id == user_id).options(selectinload(User.projects))
        )
        user = result.scalars().first()

        if user:
            for key, value in user_update.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            await db.commit()
            await db.refresh(user)
        return user

    # DELETE
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if user:
            await db.delete(user)
            await db.commit()
            return True
        return False
