from fastapi import FastAPI
from app.api.v1.routes import routers
from app.core.exception_handlers import message_exception_handler
from app.core.exceptions import MessageException

app = FastAPI()
app.include_router(routers)
app.add_exception_handler(MessageException, message_exception_handler)

