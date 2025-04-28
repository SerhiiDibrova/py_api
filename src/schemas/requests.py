from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    value: str


class ProductCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int


class OrderCreateRequest(BaseModel):
    user_email: EmailStr
    product_ids: List[UUID]