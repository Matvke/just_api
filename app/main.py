from fastapi import FastAPI, Request
from app.api.v1.routes import routers
from app.core.exception_handlers import message_exception_handler
from app.core.exceptions import MessageException

app = FastAPI()
app.include_router(routers)
app.add_exception_handler(MessageException, message_exception_handler)

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Method"] = str(request.method)
    return response