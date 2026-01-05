from fastapi import APIRouter
from app.modules.marketing.api.fast_api import router as marketing_router

router = APIRouter()
router.include_router(marketing_router, prefix="/marketing", tags=["Marketing"])