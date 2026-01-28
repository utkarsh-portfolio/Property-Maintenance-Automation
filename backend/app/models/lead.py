from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    ESTIMATE_SENT = "estimate_sent"
    NEGOTIATING = "negotiating"
    WON = "won"
    LOST = "lost"


class ServiceType(str, enum.Enum):
    HVAC = "hvac"
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    ROOFING = "roofing"
    PEST_CONTROL = "pest_control"
    REMODELING = "remodeling"
    GENERAL_MAINTENANCE = "general_maintenance"


class Lead(Base):
    """Lead model - potential service requests to be converted to jobs."""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    # Customer reference
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # Lead details
    service_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    urgency = Column(String(20), default="normal")  # low, normal, high, emergency

    # Status tracking
    status = Column(String(30), default=LeadStatus.NEW.value, index=True)
    source = Column(String(50))  # website, phone, referral, sms

    # Estimate info
    estimated_value = Column(Numeric(10, 2))
    actual_value = Column(Numeric(10, 2))

    # Follow-up
    last_contact = Column(DateTime(timezone=True))
    next_follow_up = Column(DateTime(timezone=True))
    follow_up_count = Column(Integer, default=0)

    # Notes
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True))

    # Relationships
    customer = relationship("Customer", back_populates="leads")
    appointments = relationship("Appointment", back_populates="lead")

    @property
    def is_open(self) -> bool:
        return self.status not in [LeadStatus.WON.value, LeadStatus.LOST.value]
