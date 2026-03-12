from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class FeedbackMessage(Base):
    __tablename__ = "feedback_messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    subject = Column(String(200), nullable=True)
    message = Column(Text, nullable=False)
    status = Column(Enum('new', 'in_progress', 'completed'), default='new', nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    
    # Relationships
    user = relationship("User", back_populates="feedback_messages")