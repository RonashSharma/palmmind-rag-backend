from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.database import Base

class DocumentRecord(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    chunk_strategy = Column(String, nullable=False)
    chunk_count = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class BookingRecord(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)