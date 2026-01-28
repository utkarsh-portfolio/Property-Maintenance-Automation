"""
Analytics API endpoints for dashboard metrics and reporting.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from datetime import datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.models.lead import Lead, LeadStatus
from app.models.appointment import Appointment, AppointmentStatus
from app.models.customer import Customer
from app.models.conversation import Conversation, Message

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
):
    """Get main dashboard statistics."""
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Total leads
    total_leads = await db.scalar(select(func.count(Lead.id)))

    # Leads this week
    leads_this_week = await db.scalar(
        select(func.count(Lead.id)).where(
            func.date(Lead.created_at) >= week_ago
        )
    )

    # Conversion rate (leads to appointments)
    converted_leads = await db.scalar(
        select(func.count(Lead.id)).where(
            Lead.status == LeadStatus.CONVERTED
        )
    )
    conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0

    # Today's appointments
    todays_appointments = await db.scalar(
        select(func.count(Appointment.id)).where(
            func.date(Appointment.scheduled_start) == today
        )
    )

    # Total customers
    total_customers = await db.scalar(select(func.count(Customer.id)))

    # Active conversations
    active_conversations = await db.scalar(
        select(func.count(Conversation.id)).where(
            Conversation.status == "active"
        )
    )

    # Revenue this month (from completed appointments)
    monthly_revenue = await db.scalar(
        select(func.sum(Appointment.actual_cost)).where(
            and_(
                Appointment.status == AppointmentStatus.COMPLETED,
                func.date(Appointment.completed_at) >= month_ago
            )
        )
    ) or 0

    # AI messages handled
    ai_messages = await db.scalar(
        select(func.count(Message.id)).where(
            and_(
                Message.role == "assistant",
                func.date(Message.created_at) >= week_ago
            )
        )
    )

    return {
        "leads": {
            "total": total_leads or 0,
            "this_week": leads_this_week or 0,
            "conversion_rate": round(conversion_rate, 1),
        },
        "appointments": {
            "today": todays_appointments or 0,
        },
        "customers": {
            "total": total_customers or 0,
        },
        "conversations": {
            "active": active_conversations or 0,
            "ai_messages_week": ai_messages or 0,
        },
        "revenue": {
            "this_month": float(monthly_revenue),
        },
    }


@router.get("/leads/by-status")
async def get_leads_by_status(
    db: AsyncSession = Depends(get_db),
):
    """Get lead counts grouped by status."""
    result = await db.execute(
        select(Lead.status, func.count(Lead.id))
        .group_by(Lead.status)
    )

    data = {status.value: 0 for status in LeadStatus}
    for status, count in result.all():
        data[status.value] = count

    return {"data": data}


@router.get("/leads/by-service")
async def get_leads_by_service(
    db: AsyncSession = Depends(get_db),
):
    """Get lead counts grouped by service type."""
    result = await db.execute(
        select(Lead.service_type, func.count(Lead.id))
        .group_by(Lead.service_type)
    )

    data = []
    for service_type, count in result.all():
        data.append({
            "service": service_type.value if hasattr(service_type, 'value') else service_type,
            "count": count,
        })

    return {"data": sorted(data, key=lambda x: x["count"], reverse=True)}


@router.get("/leads/trend")
async def get_leads_trend(
    days: int = Query(default=30, le=90),
    db: AsyncSession = Depends(get_db),
):
    """Get daily lead counts for trend chart."""
    start_date = datetime.utcnow().date() - timedelta(days=days)

    result = await db.execute(
        select(
            func.date(Lead.created_at).label("date"),
            func.count(Lead.id).label("count")
        )
        .where(func.date(Lead.created_at) >= start_date)
        .group_by(func.date(Lead.created_at))
        .order_by(func.date(Lead.created_at))
    )

    data = []
    for row in result.all():
        data.append({
            "date": row.date.isoformat(),
            "count": row.count,
        })

    return {"data": data}


@router.get("/appointments/by-status")
async def get_appointments_by_status(
    db: AsyncSession = Depends(get_db),
):
    """Get appointment counts grouped by status."""
    result = await db.execute(
        select(Appointment.status, func.count(Appointment.id))
        .group_by(Appointment.status)
    )

    data = {status.value: 0 for status in AppointmentStatus}
    for status, count in result.all():
        data[status.value] = count

    return {"data": data}


@router.get("/appointments/upcoming")
async def get_upcoming_appointments(
    days: int = Query(default=7, le=30),
    db: AsyncSession = Depends(get_db),
):
    """Get daily appointment counts for upcoming days."""
    today = datetime.utcnow().date()
    end_date = today + timedelta(days=days)

    result = await db.execute(
        select(
            func.date(Appointment.scheduled_start).label("date"),
            func.count(Appointment.id).label("count")
        )
        .where(
            and_(
                func.date(Appointment.scheduled_start) >= today,
                func.date(Appointment.scheduled_start) <= end_date,
                Appointment.status.in_([
                    AppointmentStatus.SCHEDULED,
                    AppointmentStatus.CONFIRMED,
                ])
            )
        )
        .group_by(func.date(Appointment.scheduled_start))
        .order_by(func.date(Appointment.scheduled_start))
    )

    data = []
    for row in result.all():
        data.append({
            "date": row.date.isoformat(),
            "count": row.count,
        })

    return {"data": data}


@router.get("/revenue/trend")
async def get_revenue_trend(
    days: int = Query(default=30, le=90),
    db: AsyncSession = Depends(get_db),
):
    """Get daily revenue for trend chart."""
    start_date = datetime.utcnow().date() - timedelta(days=days)

    result = await db.execute(
        select(
            func.date(Appointment.completed_at).label("date"),
            func.sum(Appointment.actual_cost).label("revenue")
        )
        .where(
            and_(
                Appointment.status == AppointmentStatus.COMPLETED,
                func.date(Appointment.completed_at) >= start_date
            )
        )
        .group_by(func.date(Appointment.completed_at))
        .order_by(func.date(Appointment.completed_at))
    )

    data = []
    for row in result.all():
        data.append({
            "date": row.date.isoformat(),
            "revenue": float(row.revenue or 0),
        })

    return {"data": data}


@router.get("/ai/performance")
async def get_ai_performance(
    days: int = Query(default=7, le=30),
    db: AsyncSession = Depends(get_db),
):
    """Get AI agent performance metrics."""
    start_date = datetime.utcnow() - timedelta(days=days)

    # Total conversations
    total_conversations = await db.scalar(
        select(func.count(Conversation.id)).where(
            Conversation.created_at >= start_date
        )
    )

    # Total messages
    total_messages = await db.scalar(
        select(func.count(Message.id)).where(
            Message.created_at >= start_date
        )
    )

    # AI responses
    ai_responses = await db.scalar(
        select(func.count(Message.id)).where(
            and_(
                Message.role == "assistant",
                Message.created_at >= start_date
            )
        )
    )

    # Average response tokens
    avg_tokens = await db.scalar(
        select(func.avg(Message.tokens_used)).where(
            and_(
                Message.role == "assistant",
                Message.created_at >= start_date,
                Message.tokens_used.isnot(None)
            )
        )
    )

    # Conversations by channel
    channel_result = await db.execute(
        select(Conversation.channel, func.count(Conversation.id))
        .where(Conversation.created_at >= start_date)
        .group_by(Conversation.channel)
    )
    by_channel = {channel: count for channel, count in channel_result.all()}

    # Intent detection breakdown
    intent_result = await db.execute(
        select(Conversation.intent_detected, func.count(Conversation.id))
        .where(
            and_(
                Conversation.created_at >= start_date,
                Conversation.intent_detected.isnot(None)
            )
        )
        .group_by(Conversation.intent_detected)
    )
    by_intent = {intent: count for intent, count in intent_result.all()}

    return {
        "total_conversations": total_conversations or 0,
        "total_messages": total_messages or 0,
        "ai_responses": ai_responses or 0,
        "avg_tokens_per_response": round(avg_tokens or 0, 1),
        "by_channel": by_channel,
        "by_intent": by_intent,
    }
