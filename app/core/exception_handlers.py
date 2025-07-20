from fastapi.responses import JSONResponse
from fastapi import Request
from .exceptions import MessageException
from http import HTTPStatus

async def message_exception_handler(request: Request, exc: MessageException):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"message": exc.message},
    )