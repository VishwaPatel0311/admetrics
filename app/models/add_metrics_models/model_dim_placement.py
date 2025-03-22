from sqlalchemy import Column, Integer, String

from db import Base


class DimPlacementModel(Base):
    __tablename__ = "dim_placement"
    placement_id = Column(Integer, primary_key=True)
    placement_name = Column(String, nullable=False)