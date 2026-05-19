import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class FeedbackFormTypes(enum.Enum):
    BUG_REPORT = "bug report"
    FEATURE_REQUEST = "feature request"
    COMPLIMENT = "compliment"

class FeedbackForm(db.Model):
    __tablename__ = 'feedback_forms'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(FeedbackFormTypes))
    content = db.Column(db.String)
    submission_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))