from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"


class Appointment(Base):
    """Appointment model - scheduled service visits."""
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    # References
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    lead_id = Column(Integer, ForeignKey("leads.id"))

    # Scheduling
    scheduled_start = Column(DateTime(timezone=True), nullable=False, index=True)
    scheduled_end = Column(DateTime(timezone=True), nullable=False)
    actual_start = Column(DateTime(timezone=True))
    actual_end = Column(DateTime(timezone=True))

    # Status
    status = Column(String(30), default=AppointmentStatus.SCHEDULED.value, index=True)

    # Details
    service_type = Column(String(50), nullable=False)
    description = Column(Text)
    technician_name = Column(String(200))

    # Location (can override customer address)
    service_address = Column(String(500))

    # Reminders
    reminder_sent = Column(Boolean, default=False)
    confirmation_sent = Column(Boolean, default=False)
    customer_confirmed = Column(Boolean, default=False)

    # Notes
    notes = Column(Text)
    completion_notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="appointments")
    lead = relationship("Lead", back_populates="appointments")
