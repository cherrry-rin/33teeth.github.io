from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.db.base import Base


class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=True)
    duration = Column(Integer, nullable=True)  # длительность в минутах
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    
    # Relationships
    appointments = relationship("Appointment", back_populates="service")