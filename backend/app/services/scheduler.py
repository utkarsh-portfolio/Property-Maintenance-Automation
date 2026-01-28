"""
Background task scheduler for automated operations.
Handles: appointment reminders, lead follow-ups, analytics reports.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.models.appointment import Appointment, AppointmentStatus
from app.models.lead import Lead, LeadStatus
from app.models.customer import Customer
from app.services.email_service import email_service
from app.services.twilio_service import twilio_service


class SchedulerService:
    """Background task scheduler for automated operations."""

    def __init__(self):
        self.running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Start the scheduler."""
        if self.running:
            return
        self.running = True
        self._task = asyncio.create_task(self._run_scheduler())
        print("Scheduler started")

    async def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        print("Scheduler stopped")

    async def _run_scheduler(self):
        """Main scheduler loop - runs tasks at intervals."""
        while self.running:
            try:
                # Run tasks
                await self._send_appointment_reminders()
                await self._follow_up_stale_leads()

                # Wait 1 hour before next run
                await asyncio.sleep(3600)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Scheduler error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

    async def _send_appointment_reminders(self):
        """Send reminders for appointments happening in 24 hours."""
        async with async_session() as db:
            tomorrow = datetime.utcnow() + timedelta(hours=24)
            tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0)
            tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59)

            # Find appointments tomorrow that haven't been reminded
            result = await db.execute(
                select(Appointment)
                .where(
                    and_(
                        Appointment.scheduled_start >= tomorrow_start,
                        Appointment.scheduled_start <= tomorrow_end,
                        Appointment.status.in_([
                            AppointmentStatus.SCHEDULED,
                            AppointmentStatus.CONFIRMED,
                        ]),
                        Appointment.reminder_sent == False,
                    )
                )
            )
            appointments = result.scalars().all()

            for appointment in appointments:
                # Get customer info
                customer_result = await db.execute(
                    select(Customer).where(Customer.id == appointment.customer_id)
                )
                customer = customer_result.scalar_one_or_none()

                if not customer:
                    continue

                # Send email reminder
                if customer.email:
                    await email_service.send_appointment_reminder(
                        customer_email=customer.email,
                        customer_name=customer.full_name,
                        service_type=appointment.service_type.value,
                        scheduled_date=appointment.scheduled_start.strftime("%B %d, %Y"),
                        scheduled_time=appointment.scheduled_start.strftime("%I:%M %p"),
                    )

                # Send SMS reminder
                if customer.phone:
                    message = (
                        f"Hi {customer.first_name}! Reminder: Your "
                        f"{appointment.service_type.value.replace('_', ' ')} appointment is "
                        f"tomorrow at {appointment.scheduled_start.strftime('%I:%M %p')}. "
                        f"Reply CONFIRM to confirm or RESCHEDULE to change."
                    )
                    await twilio_service.send_sms(customer.phone, message)

                # Mark reminder as sent
                appointment.reminder_sent = True

            await db.commit()
            print(f"Sent {len(appointments)} appointment reminders")

    async def _follow_up_stale_leads(self):
        """Follow up on leads that haven't been contacted in 3 days."""
        async with async_session() as db:
            stale_date = datetime.utcnow() - timedelta(days=3)

            # Find stale leads
            result = await db.execute(
                select(Lead)
                .where(
                    and_(
                        Lead.status.in_([
                            LeadStatus.NEW,
                            LeadStatus.CONTACTED,
                            LeadStatus.ESTIMATE_SENT,
                        ]),
                        Lead.last_contacted_at < stale_date,
                        Lead.follow_up_count < 3,  # Max 3 follow-ups
                    )
                )
                .limit(50)  # Process in batches
            )
            leads = result.scalars().all()

            for lead in leads:
                # Get customer info
                customer_result = await db.execute(
                    select(Customer).where(Customer.id == lead.customer_id)
                )
                customer = customer_result.scalar_one_or_none()

                if not customer:
                    continue

                # Send follow-up email
                if customer.email:
                    await email_service.send_lead_follow_up(
                        customer_email=customer.email,
                        customer_name=customer.full_name,
                        service_type=lead.service_type.value,
                        estimate_amount=lead.estimated_value,
                    )

                # Update lead
                lead.follow_up_count = (lead.follow_up_count or 0) + 1
                lead.last_contacted_at = datetime.utcnow()

            await db.commit()
            print(f"Sent {len(leads)} lead follow-ups")

    async def send_immediate_confirmation(
        self,
        appointment_id: int,
    ):
        """Send immediate appointment confirmation (called when appointment is created)."""
        async with async_session() as db:
            # Get appointment
            result = await db.execute(
                select(Appointment).where(Appointment.id == appointment_id)
            )
            appointment = result.scalar_one_or_none()

            if not appointment:
                return

            # Get customer
            customer_result = await db.execute(
                select(Customer).where(Customer.id == appointment.customer_id)
            )
            customer = customer_result.scalar_one_or_none()

            if not customer:
                return

            # Send email confirmation
            if customer.email:
                await email_service.send_appointment_confirmation(
                    customer_email=customer.email,
                    customer_name=customer.full_name,
                    service_type=appointment.service_type.value,
                    scheduled_date=appointment.scheduled_start.strftime("%B %d, %Y"),
                    scheduled_time=appointment.scheduled_start.strftime("%I:%M %p"),
                    address=customer.full_address,
                )

            # Send SMS confirmation
            if customer.phone:
                message = (
                    f"Hi {customer.first_name}! Your {appointment.service_type.value.replace('_', ' ')} "
                    f"appointment is confirmed for {appointment.scheduled_start.strftime('%b %d at %I:%M %p')}. "
                    f"We'll send a reminder 24 hours before. Reply HELP for assistance."
                )
                await twilio_service.send_sms(customer.phone, message)


# Singleton instance
scheduler = SchedulerService()
