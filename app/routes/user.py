from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud.user import UserCRUD
from app.schemas.project import ProjectRead
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.database import get_async_session


router = APIRouter()

# Create a new user
@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    return await UserCRUD.create_user(db=db, user=user)

# Get user by ID
@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await UserCRUD.get_user_by_id(db=db, user_id=user_id)

# Update user
@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_async_session)):
    return await UserCRUD.update_user(db=db, user_id=user_id, user_update=user)

# Delete user
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    success = await UserCRUD.delete_user(db=db, user_id=user_id)
    return {"deleted": success}

# Get all projects by user ID
@router.get("/{user_id}/projects", response_model=List[ProjectRead])
async def read_projects_by_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await UserCRUD.get_projects_by_user_id(db=db, user_id=user_id)

