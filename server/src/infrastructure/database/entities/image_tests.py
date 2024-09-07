import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from infrastructure.database.entities import Base

class ImageTests(Base):
    __tablename__ = 'image_tests'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    test = relationship("Tests", back_populates="image_tests")
    test_id = Column(Integer, ForeignKey('tests.id'))
    created_at = Column(DateTime, default=lambda: datetime.datetime.now().replace(tzinfo=None))
