from typing import List, Optional

from pydantic import BaseModel

from src.schemas.models import User, Product, Order


class ServiceBaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    errors: Optional[List[str]] = None


class UserListResponse(ServiceBaseResponse):
    data: List[User]


class UserResponse(ServiceBaseResponse):
    data: User


class ProductListResponse(ServiceBaseResponse):
    data: List[Product]


class ProductResponse(ServiceBaseResponse):
    data: Product


class OrderListResponse(ServiceBaseResponse):
    data: List[Order]


class OrderResponse(ServiceBaseResponse):
    data: Order