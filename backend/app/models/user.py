from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(Enum('patient', 'admin', 'dentist'), default='patient', nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    
    # Relationships
    feedback_messages = relationship("FeedbackMessage", back_populates="user", cascade="all, delete-orphan")
    appointments = relationship("Appointment", foreign_keys="Appointment.user_id", back_populates="user", cascade="all, delete-orphan")
    dentist_appointments = relationship("Appointment", foreign_keys="Appointment.dentist_id", back_populates="dentist")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")