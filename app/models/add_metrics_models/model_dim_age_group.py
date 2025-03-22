from sqlalchemy import Column, Integer, String

from db import Base


class DimAgeGroupModel(Base):
    __tablename__ = "dim_age_group"
    age_id = Column(Integer, primary_key=True)
    age_range = Column(String, nullable=False)
