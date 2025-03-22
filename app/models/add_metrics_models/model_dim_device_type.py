from sqlalchemy import Integer, String, Column

from db import Base


class DimDeviceTypeModel(Base):
    __tablename__ = "dim_device_type"
    device_type_id = Column(Integer, primary_key=True)
    device_type_name = Column(String, nullable=False)