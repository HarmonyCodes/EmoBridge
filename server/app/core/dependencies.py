from app import models
from app.db import get_session
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """מגביל את הגישה למשתמשי ניהול בלבד."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


def ensure_self_or_admin(current_user: models.User, target_user_id: int) -> None:
    """
    מאמת שהמשתמש פועל על הרשומה של עצמו, אלא אם כן הוא אדמין.
    זורק 403 אחרת.
    """
    if current_user.id != target_user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access another user",
        )
