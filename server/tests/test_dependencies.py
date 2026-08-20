import asyncio

import pytest
from fastapi import HTTPException

from app.core.dependencies import ensure_self_or_admin, get_current_admin_user
from app.models.user import User


def _user(user_id: int, is_admin: bool = False) -> User:
    return User(
        id=user_id,
        username=f"user{user_id}",
        hashed_password="x",
        is_admin=is_admin,
    )


def test_admin_dependency_allows_admin():
    admin = _user(1, is_admin=True)

    result = asyncio.run(get_current_admin_user(current_user=admin))

    assert result is admin


def test_admin_dependency_rejects_regular_user():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(get_current_admin_user(current_user=_user(5)))

    assert exc_info.value.status_code == 403


def test_self_or_admin_allows_own_record():
    ensure_self_or_admin(_user(5), target_user_id=5)


def test_self_or_admin_allows_admin_on_any_record():
    ensure_self_or_admin(_user(1, is_admin=True), target_user_id=99)


def test_self_or_admin_rejects_foreign_record():
    with pytest.raises(HTTPException) as exc_info:
        ensure_self_or_admin(_user(5), target_user_id=99)

    assert exc_info.value.status_code == 403
