from fastapi import APIRouter

from auth.auth_config import auth_backend, fastapi_users_settings
from auth.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users_settings.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users_settings.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users_settings.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
