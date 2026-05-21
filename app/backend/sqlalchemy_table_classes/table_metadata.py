from sqlalchemy import Column, String, DateTime
from ..database import Base

class TableMetadata(Base):
    __tablename__ = 'table_metadata'

    table_name = Column(String, primary_key=True)
    last_touched = Column(DateTime)