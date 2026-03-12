from sqlalchemy import Column, Integer, TIMESTAMP, text, Enum, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.db.base import Base


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    dentist_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    appointment_date = Column(TIMESTAMP, nullable=False)
    status = Column(Enum('scheduled', 'confirmed', 'completed', 'cancelled'), default='scheduled', nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="appointments")
    dentist = relationship("User", foreign_keys=[dentist_id], back_populates="dentist_appointments")
    service = relationship("Service", back_populates="appointments")
    review = relationship("Review", back_populates="appointment", uselist=False)