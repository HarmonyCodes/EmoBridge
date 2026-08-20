import asyncio
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from app.models.user import User
from app.routers import user_router
from app.schemas import UserCreate


def _user(user_id: int, is_admin: bool = False) -> User:
    return User(
        id=user_id,
        username=f"user{user_id}",
        hashed_password="x",
        is_admin=is_admin,
    )


def test_registration_stays_public():
    """הרשמה חייבת להישאר פתוחה, אחרת אין דרך ליצור משתמש ראשון."""
    user_in = UserCreate(username="new", email="new@example.com", password="pw")
    created = _user(7)

    async def run():
        with patch("app.services.user_service.create_user", new=AsyncMock(return_value=created)) as mock_fn:
            result = await user_router.create_user(user_in, db=None)
            mock_fn.assert_awaited()
            assert result is created

    asyncio.run(run())


def test_read_user_allows_own_record():
    target = _user(5)

    async def run():
        with patch("app.services.user_service.get_user", new=AsyncMock(return_value=target)) as mock_fn:
            result = await user_router.read_user(5, current_user=_user(5), db=None)
            mock_fn.assert_awaited()
            assert result is target

    asyncio.run(run())


def test_read_user_rejects_foreign_record():
    async def run():
        with patch("app.services.user_service.get_user", new=AsyncMock()) as mock_fn:
            with pytest.raises(HTTPException) as exc_info:
                await user_router.read_user(99, current_user=_user(5), db=None)
            assert exc_info.value.status_code == 403
            # ההרשאה נבדקת לפני הפנייה לשירות, כדי לא לחשוף קיום רשומה
            mock_fn.assert_not_awaited()

    asyncio.run(run())


def test_read_user_allows_admin_on_foreign_record():
    target = _user(99)

    async def run():
        with patch("app.services.user_service.get_user", new=AsyncMock(return_value=target)) as mock_fn:
            result = await user_router.read_user(99, current_user=_user(1, is_admin=True), db=None)
            mock_fn.assert_awaited()
            assert result is target

    asyncio.run(run())


def test_delete_user_rejects_foreign_record():
    async def run():
        with patch("app.services.user_service.delete_user", new=AsyncMock()) as mock_fn:
            with pytest.raises(HTTPException) as exc_info:
                await user_router.delete_user(99, current_user=_user(5), db=None)
            assert exc_info.value.status_code == 403
            mock_fn.assert_not_awaited()

    asyncio.run(run())
