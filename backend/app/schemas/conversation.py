from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MessageBase(BaseModel):
    """Base message schema."""
    role: str  # user, assistant, system
    content: str


class MessageCreate(MessageBase):
    """Schema for creating a message."""
    pass


class MessageResponse(MessageBase):
    """Schema for message response."""
    id: int
    conversation_id: int
    tokens_used: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    """Base conversation schema."""
    customer_id: Optional[int] = None
    channel: str  # sms, voice, web_chat
    phone_number: Optional[str] = None


class ConversationCreate(ConversationBase):
    """Schema for creating a conversation."""
    initial_message: Optional[str] = None


class ConversationResponse(ConversationBase):
    """Schema for conversation response."""
    id: int
    external_id: Optional[str] = None
    status: str
    intent_detected: Optional[str] = None
    sentiment: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Schema for chat API request."""
    conversation_id: Optional[int] = None
    message: str = Field(..., min_length=1)
    customer_id: Optional[int] = None
    channel: str = "web_chat"


class ChatResponse(BaseModel):
    """Schema for chat API response."""
    conversation_id: int
    response: str
    intent: Optional[str] = None
    suggested_actions: List[str] = []


class SMSWebhook(BaseModel):
    """Schema for Twilio SMS webhook."""
    From: str
    To: str
    Body: str
    MessageSid: str
    AccountSid: Optional[str] = None
