"""
Email notification service using free SMTP providers.
Supports: Gmail, SendGrid (free tier), Mailgun (free tier)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from app.core.config import settings


class EmailService:
    """Service for sending email notifications."""

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
    ) -> bool:
        """Send an email notification."""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email

            # Plain text version
            msg.attach(MIMEText(body, "plain"))

            # HTML version (optional)
            if html_body:
                msg.attach(MIMEText(html_body, "html"))

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_email, to_email, msg.as_string())

            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

    async def send_appointment_confirmation(
        self,
        customer_email: str,
        customer_name: str,
        service_type: str,
        scheduled_date: str,
        scheduled_time: str,
        address: str,
    ) -> bool:
        """Send appointment confirmation email."""
        subject = f"Appointment Confirmed - {service_type.replace('_', ' ').title()}"

        body = f"""
Hi {customer_name},

Your appointment has been confirmed!

Service: {service_type.replace('_', ' ').title()}
Date: {scheduled_date}
Time: {scheduled_time}
Address: {address}

Our technician will arrive at the scheduled time. Please ensure someone is available to provide access.

Need to reschedule? Reply to this email or call us.

Thank you for choosing PropertyPro Maintenance!

Best regards,
PropertyPro Team
        """

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9fafb; padding: 20px; border: 1px solid #e5e7eb; }}
        .details {{ background: white; padding: 15px; border-radius: 8px; margin: 15px 0; }}
        .detail-row {{ display: flex; padding: 8px 0; border-bottom: 1px solid #f3f4f6; }}
        .label {{ font-weight: bold; color: #6b7280; width: 100px; }}
        .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0;">✅ Appointment Confirmed</h1>
        </div>
        <div class="content">
            <p>Hi <strong>{customer_name}</strong>,</p>
            <p>Great news! Your appointment has been confirmed.</p>

            <div class="details">
                <div class="detail-row">
                    <span class="label">Service:</span>
                    <span>{service_type.replace('_', ' ').title()}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Date:</span>
                    <span>{scheduled_date}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Time:</span>
                    <span>{scheduled_time}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Address:</span>
                    <span>{address}</span>
                </div>
            </div>

            <p>Our technician will arrive at the scheduled time. Please ensure someone is available.</p>
            <p>Need to reschedule? Simply reply to this email.</p>
        </div>
        <div class="footer">
            <p>PropertyPro Maintenance | Your Trusted Home Service Partner</p>
        </div>
    </div>
</body>
</html>
        """

        return await self.send_email(customer_email, subject, body, html_body)

    async def send_appointment_reminder(
        self,
        customer_email: str,
        customer_name: str,
        service_type: str,
        scheduled_date: str,
        scheduled_time: str,
        hours_until: int = 24,
    ) -> bool:
        """Send appointment reminder email."""
        subject = f"Reminder: Appointment Tomorrow - {service_type.replace('_', ' ').title()}"

        body = f"""
Hi {customer_name},

This is a friendly reminder about your upcoming appointment:

Service: {service_type.replace('_', ' ').title()}
Date: {scheduled_date}
Time: {scheduled_time}

Please ensure someone is available to provide access to our technician.

See you soon!

PropertyPro Team
        """

        return await self.send_email(customer_email, subject, body)

    async def send_lead_follow_up(
        self,
        customer_email: str,
        customer_name: str,
        service_type: str,
        estimate_amount: Optional[float] = None,
    ) -> bool:
        """Send follow-up email for unconverted leads."""
        subject = f"Following Up - Your {service_type.replace('_', ' ').title()} Inquiry"

        estimate_text = ""
        if estimate_amount:
            estimate_text = f"\n\nYour estimate: ${estimate_amount:,.2f}"

        body = f"""
Hi {customer_name},

We wanted to follow up on your recent inquiry about {service_type.replace('_', ' ')} services.
{estimate_text}

We're here to help whenever you're ready to move forward. If you have any questions or would like to schedule service, simply reply to this email or give us a call.

As a reminder, we offer:
• Free estimates
• Flexible scheduling
• Licensed and insured technicians
• Satisfaction guaranteed

Looking forward to serving you!

Best regards,
PropertyPro Team
        """

        return await self.send_email(customer_email, subject, body)


# Singleton instance
email_service = EmailService()
