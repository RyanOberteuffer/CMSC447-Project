import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime
from ..database import Base

class PrinterAvailabilityStatuses(enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"

class Printer(Base):
    __tablename__ = 'printers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    model = Column(String)
    curr_status = Column(Enum(PrinterAvailabilityStatuses))
    toner_level = Column(Integer)
    paper_level = Column(Integer)
    last_maintenance = Column(DateTime)
    