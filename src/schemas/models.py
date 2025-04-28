from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import List, Optional, Literal
from uuid import UUID, uuid4
class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    value: str

    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    phone: Optional[str] = None


class Product(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Unique product ID")
    name: str = Field(..., min_length=1, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price, must be > 0")
    in_stock: int = Field(..., ge=0, description="Quantity in stock, ≥ 0")


class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Unique order ID")
    user_email: EmailStr = Field(..., description="Email of the user who placed the order")
    products: List[Product] = Field(..., description="List of products in the order")
    status: Literal['pending', 'paid', 'shipped', 'delivered', 'cancelled'] = Field(
        'pending', description="Order status"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when order was created")
    total_amount: float = Field(0.0, gt=0, description="Total order amount, computed automatically")

    @validator('total_amount', always=True)
    def compute_total(cls, v, values):
        prods = values.get('products') or []
        total = sum(p.price for p in prods)
        if total <= 0:
            raise ValueError('Order total must be > 0')
        return total