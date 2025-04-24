from fastapi import FastAPI
from src import user_controller

app = FastAPI()
app.include_router(user_controller.router)
