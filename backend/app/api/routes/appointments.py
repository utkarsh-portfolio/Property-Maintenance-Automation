from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.appointment import Appointment, AppointmentStatus
from app.models.customer import Customer
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentListResponse,
    AvailableSlot,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentResponse, status_code=201)
async def create_appointment(
    appointment: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new appointment."""
    # Verify customer exists
    customer = await db.execute(
        select(Customer).where(Customer.id == appointment.customer_id)
    )
    if not customer.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Customer not found")

    # Check for scheduling conflicts
    conflict = await db.execute(
        select(Appointment).where(
            and_(
                Appointment.status.in_([
                    AppointmentStatus.SCHEDULED.value,
                    AppointmentStatus.CONFIRMED.value,
                ]),
                Appointment.scheduled_start < appointment.scheduled_end,
                Appointment.scheduled_end > appointment.scheduled_start,
            )
        )
    )
    if conflict.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="Time slot conflicts with existing appointment"
        )

    db_appointment = Appointment(**appointment.model_dump())
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment


@router.get("/", response_model=AppointmentListResponse)
async def list_appointments(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    """List appointments with pagination and filtering."""
    query = select(Appointment)

    # Apply filters
    if status:
        query = query.where(Appointment.status == status)
    if customer_id:
        query = query.where(Appointment.customer_id == customer_id)
    if date_from:
        query = query.where(Appointment.scheduled_start >= date_from)
    if date_to:
        query = query.where(Appointment.scheduled_start <= date_to)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # Apply pagination and ordering
    query = query.offset((page - 1) * per_page).limit(per_page)
    query = query.order_by(Appointment.scheduled_start.asc())

    result = await db.execute(query)
    appointments = result.scalars().all()

    return AppointmentListResponse(
        items=appointments,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/today", response_model=List[AppointmentResponse])
async def get_today_appointments(
    db: AsyncSession = Depends(get_db),
):
    """Get all appointments for today."""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    result = await db.execute(
        select(Appointment)
        .where(
            and_(
                Appointment.scheduled_start >= today_start,
                Appointment.scheduled_start < today_end,
            )
        )
        .order_by(Appointment.scheduled_start.asc())
    )
    return result.scalars().all()


@router.get("/available-slots", response_model=List[AvailableSlot])
async def get_available_slots(
    date: datetime,
    duration_minutes: int = Query(60, ge=30, le=480),
    db: AsyncSession = Depends(get_db),
):
    """Get available time slots for a given date."""
    # Business hours: 8 AM to 6 PM
    day_start = date.replace(hour=8, minute=0, second=0, microsecond=0)
    day_end = date.replace(hour=18, minute=0, second=0, microsecond=0)

    # Get existing appointments for the day
    result = await db.execute(
        select(Appointment)
        .where(
            and_(
                Appointment.scheduled_start >= day_start,
                Appointment.scheduled_start < day_end,
                Appointment.status.in_([
                    AppointmentStatus.SCHEDULED.value,
                    AppointmentStatus.CONFIRMED.value,
                ]),
            )
        )
        .order_by(Appointment.scheduled_start.asc())
    )
    existing = result.scalars().all()

    # Find available slots
    available_slots = []
    current_time = day_start

    for appt in existing:
        if current_time + timedelta(minutes=duration_minutes) <= appt.scheduled_start:
            available_slots.append(AvailableSlot(
                start=current_time,
                end=current_time + timedelta(minutes=duration_minutes),
            ))
        current_time = max(current_time, appt.scheduled_end)

    # Check remaining time after last appointment
    if current_time + timedelta(minutes=duration_minutes) <= day_end:
        available_slots.append(AvailableSlot(
            start=current_time,
            end=current_time + timedelta(minutes=duration_minutes),
        ))

    return available_slots


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get an appointment by ID."""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an appointment."""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_data = appointment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appointment, field, value)

    await db.commit()
    await db.refresh(appointment)
    return appointment


@router.post("/{appointment_id}/confirm", response_model=AppointmentResponse)
async def confirm_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Confirm an appointment (customer confirmation)."""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.customer_confirmed = True
    appointment.status = AppointmentStatus.CONFIRMED.value
    await db.commit()
    await db.refresh(appointment)
    return appointment


@router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
async def cancel_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Cancel an appointment."""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = AppointmentStatus.CANCELLED.value
    await db.commit()
    await db.refresh(appointment)
    return appointment
