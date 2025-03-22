from sqlalchemy import Column, Integer, ForeignKey, Float

from db.base_class import Base

class FactAdMetricsDailyModel(Base):

    __tablename__ = "fact_ad_metrics_daily"

    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey("dim_date.date_id"))
    region_id = Column(Integer, ForeignKey("dim_region.region_id"))
    age_id = Column(Integer, ForeignKey("dim_age_group.age_id"))
    gender_id = Column(Integer, ForeignKey("dim_gender.gender_id"))
    platform_id = Column(Integer, ForeignKey("dim_platform.platform_id"))
    placement_id = Column(Integer, ForeignKey("dim_placement.placement_id"))
    device_type_id = Column(Integer, ForeignKey("dim_device_type.device_type_id"))
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    conversions = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)
