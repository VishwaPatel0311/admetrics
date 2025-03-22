from sqlalchemy import Column, Integer, String

from db import Base


class DimGenderModel(Base):
    __tablename__ = "dim_gender"
    gender_id = Column(Integer, primary_key=True)
    gender_name = Column(String, nullable=False)