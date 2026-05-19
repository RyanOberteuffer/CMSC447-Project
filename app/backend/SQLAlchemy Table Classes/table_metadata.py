from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class TableMetadata(db.Model):
    __tablename__ = 'table_metadata'

    table_name = db.Column(db.String, primary_key=True)
    last_touched = db.Column(db.DateTime)