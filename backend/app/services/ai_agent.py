"""
AI Conversation Agent for Property Maintenance Automation.
Uses Groq (free tier) with Llama 3.1 for natural language processing.
"""
from typing import Optional, List, Dict, Any
from groq import Groq
from app.core.config import settings


class PropertyMaintenanceAgent:
    """AI agent for handling customer conversations about property maintenance."""

    SYSTEM_PROMPT = """You are a helpful AI assistant for a property maintenance company. Your role is to:

1. SCHEDULING: Help customers schedule service appointments for HVAC, plumbing, electrical, roofing, pest control, and general maintenance.

2. LEAD QUALIFICATION: Gather information about the customer's needs:
   - What service do they need?
   - What is the urgency (low, normal, high, emergency)?
   - Property address and contact details
   - Description of the issue

3. INFORMATION: Answer questions about services, pricing, and availability.

4. FOLLOW-UP: Handle estimate follow-ups and convert leads to booked appointments.

GUIDELINES:
- Be friendly, professional, and concise
- Ask clarifying questions to understand the customer's needs
- Suggest appropriate services based on their description
- For emergencies (gas leaks, flooding, electrical hazards), prioritize immediate assistance
- Always confirm details before scheduling
- If you can't help, offer to connect them with a human representative

AVAILABLE SERVICES:
- HVAC: Heating, cooling, ventilation repair and maintenance
- Plumbing: Pipes, drains, water heaters, fixtures
- Electrical: Wiring, outlets, panels, lighting
- Roofing: Repairs, inspections, replacements
- Pest Control: Insects, rodents, wildlife removal
- General Maintenance: Handyman services, repairs

When gathering information, extract and format it as JSON when possible:
{
    "intent": "scheduling|inquiry|complaint|follow_up|other",
    "service_type": "hvac|plumbing|electrical|roofing|pest_control|general_maintenance",
    "urgency": "low|normal|high|emergency",
    "description": "customer's issue description"
}
"""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None
        self.model = settings.LLM_MODEL

    async def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        customer_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process a chat message and return AI response.

        Args:
            message: The user's message
            conversation_history: Previous messages in the conversation
            customer_context: Additional context about the customer

        Returns:
            Dictionary with response, detected intent, and suggested actions
        """
        if not self.client:
            # Fallback response when API key not configured
            return self._fallback_response(message)

        # Build messages array
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

        # Add customer context if available
        if customer_context:
            context_msg = f"Customer context: {customer_context}"
            messages.append({"role": "system", "content": context_msg})

        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)

        # Add current message
        messages.append({"role": "user", "content": message})

        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

            ai_response = response.choices[0].message.content

            # Detect intent from response
            intent = self._detect_intent(message, ai_response)
            actions = self._suggest_actions(intent, message)

            return {
                "response": ai_response,
                "intent": intent,
                "suggested_actions": actions,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
            }

        except Exception as e:
            print(f"AI Agent error: {e}")
            return self._fallback_response(message)

    def _detect_intent(self, user_message: str, ai_response: str) -> str:
        """Detect the user's intent from the message."""
        message_lower = user_message.lower()

        # Emergency detection
        emergency_keywords = ["emergency", "urgent", "gas leak", "flooding", "fire", "sparks", "no heat", "no ac"]
        if any(kw in message_lower for kw in emergency_keywords):
            return "emergency"

        # Scheduling intent
        schedule_keywords = ["schedule", "appointment", "book", "available", "when can", "come out"]
        if any(kw in message_lower for kw in schedule_keywords):
            return "scheduling"

        # Inquiry intent
        inquiry_keywords = ["how much", "cost", "price", "do you", "can you", "what services"]
        if any(kw in message_lower for kw in inquiry_keywords):
            return "inquiry"

        # Complaint intent
        complaint_keywords = ["complaint", "unhappy", "problem", "issue", "not satisfied", "bad"]
        if any(kw in message_lower for kw in complaint_keywords):
            return "complaint"

        # Follow-up intent
        followup_keywords = ["estimate", "quote", "follow up", "status", "update"]
        if any(kw in message_lower for kw in followup_keywords):
            return "follow_up"

        return "general"

    def _suggest_actions(self, intent: str, message: str) -> List[str]:
        """Suggest actions based on detected intent."""
        actions = []

        if intent == "emergency":
            actions.append("transfer_to_emergency_line")
            actions.append("create_urgent_lead")

        elif intent == "scheduling":
            actions.append("show_available_slots")
            actions.append("create_appointment")

        elif intent == "inquiry":
            actions.append("show_service_info")
            actions.append("create_lead")

        elif intent == "follow_up":
            actions.append("check_estimate_status")
            actions.append("schedule_follow_up")

        elif intent == "complaint":
            actions.append("transfer_to_manager")
            actions.append("create_ticket")

        return actions

    def _fallback_response(self, message: str) -> Dict[str, Any]:
        """Provide fallback response when AI is not available."""
        message_lower = message.lower()

        # Simple keyword matching for fallback
        if any(kw in message_lower for kw in ["schedule", "appointment", "book"]):
            response = (
                "I'd be happy to help you schedule an appointment! "
                "To get you set up, I'll need:\n"
                "1. The type of service you need (HVAC, plumbing, electrical, etc.)\n"
                "2. A brief description of the issue\n"
                "3. Your preferred date and time\n\n"
                "What service do you need help with?"
            )
            intent = "scheduling"
        elif any(kw in message_lower for kw in ["emergency", "urgent", "leak", "flood"]):
            response = (
                "I understand this is urgent! For emergencies, please call our "
                "24/7 emergency line immediately. A technician will be dispatched "
                "as soon as possible. What is the nature of your emergency?"
            )
            intent = "emergency"
        elif any(kw in message_lower for kw in ["price", "cost", "estimate"]):
            response = (
                "I can help you get an estimate! Our pricing depends on the type "
                "of service and scope of work. Could you tell me:\n"
                "1. What service do you need?\n"
                "2. What's the issue you're experiencing?\n\n"
                "This will help us provide an accurate estimate."
            )
            intent = "inquiry"
        else:
            response = (
                "Hello! I'm here to help with your property maintenance needs. "
                "I can assist you with:\n"
                "- Scheduling service appointments\n"
                "- Getting estimates\n"
                "- Answering questions about our services\n\n"
                "How can I help you today?"
            )
            intent = "general"

        return {
            "response": response,
            "intent": intent,
            "suggested_actions": self._suggest_actions(intent, message),
            "tokens_used": 0,
        }

    def extract_service_details(self, message: str) -> Dict[str, Any]:
        """Extract service details from a message."""
        message_lower = message.lower()
        details = {
            "service_type": None,
            "urgency": "normal",
            "description": message,
        }

        # Detect service type
        service_keywords = {
            "hvac": ["hvac", "heating", "cooling", "ac", "air conditioning", "furnace", "heat pump"],
            "plumbing": ["plumbing", "pipe", "drain", "water heater", "faucet", "toilet", "leak"],
            "electrical": ["electrical", "wiring", "outlet", "switch", "panel", "lights", "breaker"],
            "roofing": ["roof", "shingle", "gutter", "leak from ceiling"],
            "pest_control": ["pest", "bug", "insect", "rodent", "mouse", "rat", "ant", "termite"],
            "general_maintenance": ["handyman", "repair", "fix", "maintenance", "general"],
        }

        for service, keywords in service_keywords.items():
            if any(kw in message_lower for kw in keywords):
                details["service_type"] = service
                break

        # Detect urgency
        if any(kw in message_lower for kw in ["emergency", "urgent", "asap", "immediately"]):
            details["urgency"] = "emergency"
        elif any(kw in message_lower for kw in ["soon", "quick", "today", "tomorrow"]):
            details["urgency"] = "high"
        elif any(kw in message_lower for kw in ["whenever", "no rush", "next week"]):
            details["urgency"] = "low"

        return details


# Global agent instance
ai_agent = PropertyMaintenanceAgent()
