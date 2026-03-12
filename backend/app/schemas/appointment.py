from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AppointmentBase(BaseModel):
    user_id: int
    service_id: int
    dentist_id: Optional[int] = None
    appointment_date: datetime
    status: Optional[str] = "scheduled"
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    dentist_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentInDBBase(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Appointment(AppointmentInDBBase):
    pass