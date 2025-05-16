from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, get_user
from pydantic import BaseModel, validator
from typing import List

from src.services import ProductService
from src.schemas import ProductDTO, PageRequest

router = APIRouter()

@router.post("/products", response_model=ProductDTO, status_code=status.HTTP_201_CREATED)
async def create_product(product_dto: ProductDTO, service: ProductService = Depends()):
    try:
        if not product_dto.is_valid():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product data")
        created_product = await service.create_product(product_dto)
        return created_product
    except Exception as e:
        if isinstance(e, ValueError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        elif isinstance(e, RuntimeError):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/products", response_model=List[ProductDTO])
async def get_products(page_request: PageRequest, service: ProductService = Depends()):
    try:
        if not page_request.is_valid():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid page request")
        products = await service.get_products(page_request)
        return products
    except Exception as e:
        if isinstance(e, ValueError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        elif isinstance(e, RuntimeError):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))