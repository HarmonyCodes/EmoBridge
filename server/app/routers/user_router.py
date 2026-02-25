from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserRead, ProgressRead, ProgressCreate
from app.services.user_service import create_user, list_users, get_user, update_user, delete_user
from app.db import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    return await services.user_service.create_user(db, user_in)


@router.get("/", response_model=List[schemas.UserRead])
async def list_users(limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await services.user_service.list_users(db, limit=limit)


@router.get("/{user_id}", response_model=schemas.UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await services.user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=schemas.UserRead)
async def update_user(user_id: int, user_in: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    user = await services.user_service.update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    ok = await services.user_service.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}
