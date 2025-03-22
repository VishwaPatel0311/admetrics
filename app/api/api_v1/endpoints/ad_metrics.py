from typing import Optional, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import dao
from api import deps
from core import create_error_response
from descriptions import GET_AD_METRICS, AD_METRICS_DATA
from schemas.ad_metrics.ad_metrics_response import MetricsResponse, ErrorResponse, InsertMetricsResponse

ad_metrics_router = APIRouter(prefix='/admetrics', tags=["Ad Metrics Api"])

@ad_metrics_router.post('/add_metrics_data', name="Inserts Dummy data for testing purpose",
                        description=AD_METRICS_DATA,
                        response_model=Union[InsertMetricsResponse, ErrorResponse])
def add_metrics_data(*, db:Session = Depends(deps.get_db)):
    """
    API will insert dummy data in tables fact_ad_metrics_daily, dim_gender, dim_age_group,
    dim_date, dim_device_type, dim_placement, dim_platform, dim_region.
    @param db:
    @return:
    """
    try:
        response = dao.insert_dummy_ad_metrics_data(db)
        return response
    except Exception as e:
        print(f"Exception occurred in add_metrics_data: {str(e)}")
        return create_error_response(error=100, msg=str(e))


@ad_metrics_router.get('/get_ad_metrics',
                         name="Gets All Add metrics data with filters",
                         description=GET_AD_METRICS,
                       response_model=Union[MetricsResponse, ErrorResponse])
def get_ad_metrics_data(*, db: Session = Depends(deps.get_db),
                        filters: Optional[str] = Query(None, description="JSON string of filters"),
                        page: int = Query(None),
                        size: int = Query(None),):
    """
    API will be used to get the data for ad metrics with filters and paginations.
    """
    try:
        response = dao.get_ad_metrics_data(db, filters=filters,
                                            page=page,
                                            size=size)

        return response
    except Exception as e:
        print(f"Exception occurred in get_ad_metrics_data: {str(e)}")
        return create_error_response(error=100, msg=str(e))
