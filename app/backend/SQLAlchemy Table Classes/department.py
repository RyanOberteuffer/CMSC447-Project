from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=False)
    faculty_head = db.Column(db.String(100), nullable=False)
    office_location = db.Column(db.String(100), nullable=False)