from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True) # Optional if OAuth
    is_active = Column(Boolean, default=True)
    subscription_plan = Column(String, default="free") # free, pro
    created_at = Column(DateTime, default=datetime.utcnow)

class ConversionJob(Base):
    __tablename__ = "conversion_jobs"
    
    id = Column(String, primary_key=True, index=True) # UUID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for guest uploads
    original_filename = Column(String)
    status = Column(String, default="uploaded") # uploaded, queued, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
