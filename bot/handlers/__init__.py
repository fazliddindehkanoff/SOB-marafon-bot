from aiogram import Router

from .start import router as start_router
from .user import user_router
from .admin import admin_router

router = Router()
router.include_router(start_router)
router.include_router(user_router)
router.include_router(admin_router)
