from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.core.database import get_db
from app.models.lead import Lead, LeadStatus
from app.models.customer import Customer
from app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
    LeadListResponse,
    LeadStats,
)

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("/", response_model=LeadResponse, status_code=201)
async def create_lead(
    lead: LeadCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new lead."""
    # Verify customer exists
    customer = await db.execute(
        select(Customer).where(Customer.id == lead.customer_id)
    )
    if not customer.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Customer not found")

    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    await db.commit()
    await db.refresh(db_lead)
    return db_lead


@router.get("/", response_model=LeadListResponse)
async def list_leads(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    service_type: Optional[str] = None,
    customer_id: Optional[int] = None,
    urgency: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List leads with pagination and filtering."""
    query = select(Lead)

    # Apply filters
    if status:
        query = query.where(Lead.status == status)
    if service_type:
        query = query.where(Lead.service_type == service_type)
    if customer_id:
        query = query.where(Lead.customer_id == customer_id)
    if urgency:
        query = query.where(Lead.urgency == urgency)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # Apply pagination and ordering
    query = query.offset((page - 1) * per_page).limit(per_page)
    query = query.order_by(Lead.created_at.desc())

    result = await db.execute(query)
    leads = result.scalars().all()

    return LeadListResponse(
        items=leads,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/stats", response_model=LeadStats)
async def get_lead_stats(
    db: AsyncSession = Depends(get_db),
):
    """Get lead statistics."""
    # Total leads
    total = (await db.execute(select(func.count(Lead.id)))).scalar()

    # Leads by status
    async def count_by_status(status: str) -> int:
        result = await db.execute(
            select(func.count(Lead.id)).where(Lead.status == status)
        )
        return result.scalar() or 0

    new_leads = await count_by_status(LeadStatus.NEW.value)
    qualified = await count_by_status(LeadStatus.QUALIFIED.value)
    won = await count_by_status(LeadStatus.WON.value)
    lost = await count_by_status(LeadStatus.LOST.value)

    # Conversion rate
    closed = won + lost
    conversion_rate = (won / closed * 100) if closed > 0 else 0

    # Total value of won leads
    value_result = await db.execute(
        select(func.sum(Lead.actual_value)).where(Lead.status == LeadStatus.WON.value)
    )
    total_value = value_result.scalar() or Decimal("0")

    return LeadStats(
        total_leads=total,
        new_leads=new_leads,
        qualified_leads=qualified,
        won_leads=won,
        lost_leads=lost,
        conversion_rate=round(conversion_rate, 2),
        total_value=total_value,
    )


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a lead by ID."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    update_data = lead_update.model_dump(exclude_unset=True)

    # Track status changes
    if "status" in update_data:
        new_status = update_data["status"]
        if new_status in [LeadStatus.WON.value, LeadStatus.LOST.value]:
            lead.closed_at = datetime.utcnow()

    # Update last contact if status changed
    if "status" in update_data and update_data["status"] != lead.status:
        lead.last_contact = datetime.utcnow()
        lead.follow_up_count += 1

    for field, value in update_data.items():
        setattr(lead, field, value)

    await db.commit()
    await db.refresh(lead)
    return lead


@router.post("/{lead_id}/follow-up", response_model=LeadResponse)
async def record_follow_up(
    lead_id: int,
    next_follow_up: Optional[datetime] = None,
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Record a follow-up on a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.last_contact = datetime.utcnow()
    lead.follow_up_count += 1
    if next_follow_up:
        lead.next_follow_up = next_follow_up
    if notes:
        lead.notes = f"{lead.notes}\n\n{notes}" if lead.notes else notes

    await db.commit()
    await db.refresh(lead)
    return lead
