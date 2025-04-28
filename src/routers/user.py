# src/api/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.core.database import DatabaseConnection
from src.core.dependencies import get_db_connection
from src.core.responses import error_response, success_response
from src.schemas.requests import UserCreateRequest
from src.schemas.responses import UserListResponse, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get(
    "",
    response_model=UserListResponse,
    summary="List users",
)
async def list_users(
    offset: int = 0,
    limit: int = 10,
    db: DatabaseConnection = Depends(get_db_connection),
):
    users = db.query_all(
        "SELECT * FROM users ORDER BY email LIMIT %s OFFSET %s",
        (limit, offset),
    )
    return success_response(data=users)


@router.get(
    "/{email}",
    response_model=UserResponse,
    summary="Get a single user by email",
)
async def get_user(
    email: str,
    db: DatabaseConnection = Depends(get_db_connection),
):
    user = db.query_one("SELECT * FROM users WHERE email = %s", (email,))
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return success_response(data=user)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create or update a user’s value",
)
async def create_user(
    payload: UserCreateRequest,
    db: DatabaseConnection = Depends(get_db_connection),
):
    # upsert and return the full user record
    db.execute(
        """
        INSERT INTO users (email, value)
        VALUES (%s, %s)
        ON CONFLICT (email) DO UPDATE SET value = EXCLUDED.value
        """,
        (payload.email, payload.value),
    )
    user = db.query_one("SELECT * FROM users WHERE email = %s", (payload.email,))
    return success_response(data=user)


@router.delete(
    "/{email}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
)
async def delete_user(
    email: str,
    db: DatabaseConnection = Depends(get_db_connection),
):
    db.execute("DELETE FROM users WHERE email = %s", (email,))
    return success_response()
