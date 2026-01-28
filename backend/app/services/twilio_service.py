"""
Twilio SMS/Voice Service for Property Maintenance Automation.
Handles inbound/outbound SMS and appointment reminders.
"""
from typing import Optional
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from app.core.config import settings


class TwilioService:
    """Service for handling SMS communications via Twilio."""

    def __init__(self):
        self.client = None
        self.phone_number = settings.TWILIO_PHONE_NUMBER

        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )

    @property
    def is_configured(self) -> bool:
        """Check if Twilio is properly configured."""
        return self.client is not None and bool(self.phone_number)

    async def send_sms(
        self,
        to: str,
        message: str,
    ) -> Optional[str]:
        """
        Send an SMS message.

        Args:
            to: Recipient phone number (E.164 format)
            message: Message content

        Returns:
            Message SID if successful, None otherwise
        """
        if not self.is_configured:
            print(f"[MOCK SMS] To: {to}, Message: {message}")
            return "MOCK_SID_" + to[-4:]

        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to,
            )
            return msg.sid
        except Exception as e:
            print(f"Twilio SMS error: {e}")
            return None

    async def send_appointment_reminder(
        self,
        to: str,
        customer_name: str,
        service_type: str,
        scheduled_time: str,
        appointment_id: int,
    ) -> Optional[str]:
        """Send an appointment reminder SMS."""
        message = (
            f"Hi {customer_name}! This is a reminder about your upcoming "
            f"{service_type} appointment scheduled for {scheduled_time}. "
            f"Reply YES to confirm or RESCHEDULE to change your appointment. "
            f"Ref: #{appointment_id}"
        )
        return await self.send_sms(to, message)

    async def send_appointment_confirmation(
        self,
        to: str,
        customer_name: str,
        service_type: str,
        scheduled_time: str,
        technician_name: Optional[str] = None,
    ) -> Optional[str]:
        """Send an appointment confirmation SMS."""
        tech_info = f" Your technician will be {technician_name}." if technician_name else ""
        message = (
            f"Hi {customer_name}! Your {service_type} appointment is confirmed "
            f"for {scheduled_time}.{tech_info} Reply HELP if you need assistance."
        )
        return await self.send_sms(to, message)

    async def send_estimate_follow_up(
        self,
        to: str,
        customer_name: str,
        service_type: str,
        days_since_estimate: int,
    ) -> Optional[str]:
        """Send a follow-up SMS for an unsold estimate."""
        message = (
            f"Hi {customer_name}! We wanted to follow up on the {service_type} "
            f"estimate we provided {days_since_estimate} days ago. "
            f"Do you have any questions or would you like to schedule the service? "
            f"Reply YES to book or CALL to request a callback."
        )
        return await self.send_sms(to, message)

    async def send_service_complete(
        self,
        to: str,
        customer_name: str,
        service_type: str,
    ) -> Optional[str]:
        """Send a service completion notification."""
        message = (
            f"Hi {customer_name}! Your {service_type} service has been completed. "
            f"Thank you for choosing us! We'd appreciate your feedback. "
            f"Reply with a rating from 1-5 or visit our website to leave a review."
        )
        return await self.send_sms(to, message)

    def create_response(self, message: str) -> str:
        """
        Create a TwiML response for incoming SMS.

        Args:
            message: Response message to send

        Returns:
            TwiML XML string
        """
        response = MessagingResponse()
        response.message(message)
        return str(response)


# Global service instance
twilio_service = TwilioService()
