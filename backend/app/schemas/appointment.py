from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AppointmentBase(BaseModel):
    """Base appointment schema."""
    customer_id: int
    lead_id: Optional[int] = None
    scheduled_start: datetime
    scheduled_end: datetime
    service_type: str
    description: Optional[str] = None
    technician_name: Optional[str] = None
    service_address: Optional[str] = None
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    """Schema for creating a new appointment."""
    pass


class AppointmentUpdate(BaseModel):
    """Schema for updating an appointment."""
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    status: Optional[str] = None
    technician_name: Optional[str] = None
    service_address: Optional[str] = None
    notes: Optional[str] = None
    completion_notes: Optional[str] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None


class AppointmentResponse(AppointmentBase):
    """Schema for appointment response."""
    id: int
    status: str
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    reminder_sent: bool
    confirmation_sent: bool
    customer_confirmed: bool
    completion_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AppointmentListResponse(BaseModel):
    """Schema for paginated appointment list."""
    items: list[AppointmentResponse]
    total: int
    page: int
    per_page: int


class AvailableSlot(BaseModel):
    """Available time slot for scheduling."""
    start: datetime
    end: datetime
    technician: Optional[str] = None
