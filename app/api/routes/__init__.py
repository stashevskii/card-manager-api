from fastapi import APIRouter, FastAPI
from .health import router as health_router
from .admin_card import router as admin_card_router
from .user import router as user_router
from .auth import router as auth_router
from .card import router as card_router

router = APIRouter()

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(admin_card_router)
router.include_router(card_router)


def register_main_router(app: FastAPI) -> None:
    app.include_router(router)


__all__ = ["register_main_router"]
