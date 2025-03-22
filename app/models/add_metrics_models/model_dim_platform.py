from sqlalchemy import Column, Integer, String

from db import Base


class DimPlatformModel(Base):
    __tablename__ = "dim_platform"
    platform_id = Column(Integer, primary_key=True)
    platform_name = Column(String, nullable=False)