from fastapi import APIRouter, HTTPException
from src.services.user_service import UserService

router = APIRouter()
service = UserService()

@router.get("/users")
def get_users():
    return service.get_users()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    try:
        return service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
