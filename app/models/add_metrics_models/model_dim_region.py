from sqlalchemy import Column, Integer, String

from db import Base


class DimRegionModel(Base):
    __tablename__ = "dim_region"
    region_id = Column(Integer, primary_key=True)
    region_name = Column(String, nullable=False)