from fastapi import APIRouter

from src.routers import template, user, xml_json, products, orders

api_router = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not Found"}},
)

# Health check
@api_router.get("/health", summary="Service health check")
async def health_check():
    return {"status": "ok"}

# XML/JSON conversion routes
api_router.include_router(
    xml_json.router,
    prefix="/convert",
    tags=["XML/JSON Conversion"],
)

# User routes
api_router.include_router(
    user.router,
    prefix="/users",
    tags=["Users"],
)

# Product routes
api_router.include_router(
    products.router,
    prefix="/products",
    tags=["Products"],
)

# Order routes
api_router.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"],
)

# Form template routes
api_router.include_router(
    template.router,
    prefix="/templates",
    tags=["Form Templates"],
)
