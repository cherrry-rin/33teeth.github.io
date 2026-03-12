from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: Optional[Decimal] = None
    duration: Optional[int] = None
    image_url: Optional[str] = None
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    duration: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ServiceInDBBase(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Service(ServiceInDBBase):
    pass