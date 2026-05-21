from sqlalchemy import Column, Integer, DateTime
from ..database import Base

class LibraryEntryLog(Base):
    __tablename__ = 'library_entry_logs'

    id = Column(Integer, primary_key=True)
    entry_time = Column(DateTime, nullable=False)
    entry_count = Column(Integer, nullable=False)