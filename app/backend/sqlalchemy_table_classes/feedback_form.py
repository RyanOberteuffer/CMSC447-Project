import enum
from sqlalchemy import Column, Integer, Enum, String, DateTime, ForeignKey
from ..database import Base

class FeedbackFormTypes(enum.Enum):
    BUG_REPORT = "bug report"
    FEATURE_REQUEST = "feature request"
    COMPLIMENT = "compliment"

class FeedbackForm(Base):
    __tablename__ = 'feedback_forms'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(FeedbackFormTypes))
    content = Column(String)
    submission_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))