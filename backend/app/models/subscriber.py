from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from app.db.base import Base


class Subscriber(Base):
    __tablename__ = "subscribers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    active = Column(Boolean, default=True, nullable=False)
    subscribed_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))