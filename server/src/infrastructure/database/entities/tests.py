import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from infrastructure.database.entities.base import Base
from sqlalchemy.dialects.postgresql import ENUM

class Tests(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    case_name = Column(String)
    status = Column(ENUM('pending', 'success', 'failure',  name='status_enum'), default='pending')
    image_tests = relationship("ImageTests", back_populates="test")
    message = Column(String)
    note = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now().replace(tzinfo=None))
