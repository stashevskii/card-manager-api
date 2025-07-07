from fastapi import APIRouter, FastAPI
from .card import router as card_router
from .user import router as user_router
from .auth import router as auth_router
from .card import router as card_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(card_router)


def register_main_router(app: FastAPI) -> None:
    app.include_router(router)


__all__ = ["register_main_router"]
