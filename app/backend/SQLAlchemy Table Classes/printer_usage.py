import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class PrinterJobStatuses(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
class PrinterUsage(db.Model):
    __tablename__ = 'printer_usages'

    id = db.Column(db.Integer, primary_key=True)
    pages_printed = db.Column(db.Integer, nullable=False)
    print_time = db.Column(db.DateTime, nullable=False)
    job_status = db.Column(db.Enum(PrinterJobStatuses), nullable=False)