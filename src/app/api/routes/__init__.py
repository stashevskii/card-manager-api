from fastapi import APIRouter, FastAPI
from .admin_card import router as admin_card_router
from .admin_user import router as admin_user_router
from .auth import router as auth_router
from .card import router as card_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(admin_user_router)
router.include_router(admin_card_router)
router.include_router(card_router)


def register_main_router(app: FastAPI) -> None:
    app.include_router(router)


__all__ = ["register_main_router"]
