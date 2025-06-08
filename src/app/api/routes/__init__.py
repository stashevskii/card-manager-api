from fastapi import APIRouter, FastAPI
from .admin import router as admin_router
from .auth import router as auth_router
from .card import router as card_router

router = APIRouter()

router.include_router(admin_router)
router.include_router(auth_router)
router.include_router(card_router)


def register_main_router(app: FastAPI) -> None:
    app.include_router(router)


__all__ = ["register_main_router"]
