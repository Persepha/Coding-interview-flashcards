from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from router import api_router

app = FastAPI()

origins = settings.ALLOWED_HOSTS.split(" ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
