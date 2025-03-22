from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel


class DateInfo(BaseModel):
    id: int
    name: datetime  # Assuming it should be a datetime object


class Attribute(BaseModel):
    id: int
    name: str


class Metric(BaseModel):
    id: int
    date: DateInfo
    region: Attribute
    gender: Attribute
    platform: Attribute
    placement: Attribute
    device_type: Attribute
    age_group: Attribute
    impressions: int
    clicks: int
    cost: float
    conversions: int
    likes: int


class MetricsResponseData(BaseModel):
    metrics: List[Metric]
    total_count: int


class MetricsResponse(BaseModel):
    status: str
    data: MetricsResponseData


class ErrorResponseData(BaseModel):
    error_code: int
    error_message: str

class ErrorResponse(BaseModel):
    status: str
    data: ErrorResponseData

class InsertMetricsResponseData(BaseModel):
    message: str

class InsertMetricsResponse(BaseModel):
    status: str
    data: InsertMetricsResponseData