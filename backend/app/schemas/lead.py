from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class LeadBase(BaseModel):
    """Base lead schema."""
    customer_id: int
    service_type: str
    description: str = Field(..., min_length=10)
    urgency: Optional[str] = "normal"
    source: Optional[str] = None
    estimated_value: Optional[Decimal] = None
    notes: Optional[str] = None


class LeadCreate(LeadBase):
    """Schema for creating a new lead."""
    pass


class LeadUpdate(BaseModel):
    """Schema for updating a lead."""
    service_type: Optional[str] = None
    description: Optional[str] = None
    urgency: Optional[str] = None
    status: Optional[str] = None
    estimated_value: Optional[Decimal] = None
    actual_value: Optional[Decimal] = None
    next_follow_up: Optional[datetime] = None
    notes: Optional[str] = None


class LeadResponse(LeadBase):
    """Schema for lead response."""
    id: int
    status: str
    last_contact: Optional[datetime] = None
    next_follow_up: Optional[datetime] = None
    follow_up_count: int
    actual_value: Optional[Decimal] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    """Schema for paginated lead list."""
    items: list[LeadResponse]
    total: int
    page: int
    per_page: int


class LeadStats(BaseModel):
    """Lead statistics."""
    total_leads: int
    new_leads: int
    qualified_leads: int
    won_leads: int
    lost_leads: int
    conversion_rate: float
    total_value: Decimal
