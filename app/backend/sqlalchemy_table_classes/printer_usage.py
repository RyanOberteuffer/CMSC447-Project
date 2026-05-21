import enum
from sqlalchemy import Column, Integer, DateTime, Enum
from ..database import Base

class PrinterJobStatuses(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"

class PrinterUsage(Base):
    __tablename__ = 'printer_usages'

    id = Column(Integer, primary_key=True)
    pages_printed = Column(Integer, nullable=False)
    print_time = Column(DateTime, nullable=False)
    job_status = Column(Enum(PrinterJobStatuses), nullable=False)