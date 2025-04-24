from fastapi import FastAPI
from . import user_controller

app = FastAPI()
app.include_router(user_controller.router)
