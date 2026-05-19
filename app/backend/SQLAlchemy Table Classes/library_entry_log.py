from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class LibraryEntryLogs(db.Model):
    __tablename__ = 'library_entry_logs'

    id = db.Column(db.Integer, primary_key=True)
    entry_time = db.Column(db.DateTime, nullable=False)
    entry_count = db.Column(db.Integer, nullable=False)