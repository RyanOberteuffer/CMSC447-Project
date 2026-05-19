import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class PrinterAvailabilityStatuses(enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"

class Printer(db.Model):
    __tablename__ = 'printers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    model = db.Column(db.String)
    curr_status = db.Column(db.Enum(PrinterAvailabilityStatuses))
    toner_level = db.Column(db.Integer)
    paper_level = db.Column(db.Integer)
    last_maintenance = db.Column(db.DateTime)
    