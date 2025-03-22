from fastapi import APIRouter

from api.api_v1.endpoints import ad_metrics_router

router = APIRouter()
router.include_router(ad_metrics_router)
