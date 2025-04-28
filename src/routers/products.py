from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from src.core.database import DatabaseConnection
from src.core.dependencies import get_db_connection
from src.core.responses import error_response, success_response
from src.schemas.requests import ProductCreateRequest
from src.schemas.responses import ProductListResponse, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}}
)


@router.get("", response_model=ProductListResponse, summary="List products")
async def list_products(
    db: DatabaseConnection = Depends(get_db_connection),
):
    prods = db.query_all("SELECT * FROM products ORDER BY name")
    return success_response(data=prods)


@router.get("/{product_id}", response_model=ProductResponse, summary="Get a product")
async def get_product(
    product_id: UUID,
    db: DatabaseConnection = Depends(get_db_connection),
):
    prod = db.query_one("SELECT * FROM products WHERE id = %s", (product_id,))
    if not prod:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return success_response(data=prod)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product",
)
async def create_product(
    payload: ProductCreateRequest,
    db: DatabaseConnection = Depends(get_db_connection),
):
    new = db.query_one(
        "INSERT INTO products (name, description, price, in_stock) VALUES (%s, %s, %s, %s) RETURNING *",
        (payload.name, payload.description, payload.price, payload.in_stock),
    )
    return success_response(data=new)
