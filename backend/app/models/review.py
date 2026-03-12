from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    appointment = relationship("Appointment", back_populates="review")