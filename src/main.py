from fastapi import FastAPI

from config import settings
from router import api_router

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)
