from sqlalchemy import Column, Integer, DateTime

from db import Base


class DimDateModel(Base):
    __tablename__ = "dim_date"
    date_id = Column(Integer, primary_key=True)
    date_value = Column(DateTime, nullable=False)
