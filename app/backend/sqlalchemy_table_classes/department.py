from sqlalchemy import Column, Integer, String
from ..database import Base

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(100), nullable=False)
    faculty_head = Column(String(100), nullable=False)
    office_location = Column(String(100), nullable=False)