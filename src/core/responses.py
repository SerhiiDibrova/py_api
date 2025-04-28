from typing import Any, Mapping, Optional

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse


def success_response(
    data: Optional[Any] = None,
    message: Optional[str] = None,
    status_code: int = status.HTTP_200_OK,
    headers: Optional[Mapping[str, str]] = None,
) -> JSONResponse:
    """
    Return a JSONResponse with success=True, optional data and message.
    """
    payload: dict[str, Any] = {"success": True}

    if message is not None:
        payload["message"] = message

    if data is not None:
        payload["data"] = jsonable_encoder(data)

    return JSONResponse(content=payload, status_code=status_code, headers=headers)


def error_response(
    errors: Optional[Any] = None,
    message: Optional[str] = None,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    headers: Optional[Mapping[str, str]] = None,
) -> JSONResponse:
    """
    Return a JSONResponse with success=False, optional errors list and message.
    """
    payload: dict[str, Any] = {"success": False}

    if message is not None:
        payload["message"] = message

    if errors is not None:
        payload["errors"] = jsonable_encoder(errors)

    return JSONResponse(content=payload, status_code=status_code, headers=headers)
