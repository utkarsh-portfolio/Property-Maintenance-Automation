from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ConversationChannel(str, enum.Enum):
    SMS = "sms"
    VOICE = "voice"
    WEB_CHAT = "web_chat"
    EMAIL = "email"


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Conversation(Base):
    """Conversation model - AI chat sessions with customers."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    # Customer reference
    customer_id = Column(Integer, ForeignKey("customers.id"))

    # Channel info
    channel = Column(String(20), nullable=False)  # sms, voice, web_chat
    external_id = Column(String(100), index=True)  # Twilio SID, etc.
    phone_number = Column(String(20))

    # Status
    status = Column(String(20), default="active")  # active, closed, transferred

    # AI context
    context = Column(JSON, default=dict)  # Store conversation context
    intent_detected = Column(String(50))  # scheduling, inquiry, complaint, etc.
    sentiment = Column(String(20))  # positive, neutral, negative

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True))

    # Relationships
    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", order_by="Message.created_at")


class Message(Base):
    """Message model - individual messages in a conversation."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    # Conversation reference
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)

    # Message content
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)

    # Metadata
    tokens_used = Column(Integer)
    external_id = Column(String(100))  # Twilio message SID

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
