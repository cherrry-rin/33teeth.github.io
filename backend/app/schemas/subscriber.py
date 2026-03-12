from pydantic import BaseModel, EmailStr
from datetime import datetime


class SubscriberBase(BaseModel):
    email: EmailStr
    active: bool = True


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberInDBBase(SubscriberBase):
    id: int
    subscribed_at: datetime

    class Config:
        from_attributes = True


class Subscriber(SubscriberInDBBase):
    pass