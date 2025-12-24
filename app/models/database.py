# app/models/database.py
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class InferenceRecord(Base):
    __tablename__ = "inference_records"
    id = Column(Integer, primary_key=True)
    file_id = Column(String(36), unique=True, index=True)
    original_filename = Column(String(255))
    risk_probability = Column(Float)
    advice = Column(String(512))
    raw_response = Column(JSON)
    image_url = Column(String(512))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)