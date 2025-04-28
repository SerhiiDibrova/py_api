from contextlib import asynccontextmanager
from typing import AsyncIterator, Literal, Optional

from starlette.requests import Request
from fastapi import HTTPException, status

from src.core.database import DatabaseConnection


async def get_accept_request_header(request: Request) -> Literal["*/*"] | str:
    """
    Return the client's Accept header, defaulting to '*/*' if missing.
    """
    return request.headers.get("accept", "*/*")


@asynccontextmanager
async def get_db_connection(request: Request) -> AsyncIterator[DatabaseConnection]:
    """
    Yield a per-request database connection, and close it on teardown.
    """
    db: Optional[DatabaseConnection] = request.app.state.db_connection
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not initialized"
        )
    try:
        yield db
    finally:
        db.close()
