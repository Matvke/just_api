from fastapi.responses import JSONResponse
from fastapi import Request, status
from .service_exceptions import MessageException


async def message_exception_handler(request: Request, exc: MessageException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message},
    )