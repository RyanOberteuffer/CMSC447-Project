from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Printer(db.Model):
    __tablename__ = 'printers'

    