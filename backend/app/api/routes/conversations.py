from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.database import get_db
from app.models.conversation import Conversation, Message
from app.models.customer import Customer
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ChatRequest,
    ChatResponse,
    SMSWebhook,
)
from app.services.ai_agent import ai_agent
from app.services.twilio_service import twilio_service

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message and get an AI response.
    Creates a new conversation if conversation_id is not provided.
    """
    conversation = None
    conversation_history = []

    # Get or create conversation
    if request.conversation_id:
        result = await db.execute(
            select(Conversation).where(Conversation.id == request.conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Load conversation history
        messages_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
        )
        for msg in messages_result.scalars().all():
            conversation_history.append({
                "role": msg.role,
                "content": msg.content,
            })
    else:
        # Create new conversation
        conversation = Conversation(
            customer_id=request.customer_id,
            channel=request.channel,
            status="active",
        )
        db.add(conversation)
        await db.flush()

    # Get customer context if available
    customer_context = None
    if conversation.customer_id:
        customer_result = await db.execute(
            select(Customer).where(Customer.id == conversation.customer_id)
        )
        customer = customer_result.scalar_one_or_none()
        if customer:
            customer_context = {
                "name": customer.full_name,
                "address": customer.full_address,
                "preferred_contact": customer.preferred_contact,
            }

    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
    )
    db.add(user_message)

    # Get AI response
    ai_result = await ai_agent.chat(
        message=request.message,
        conversation_history=conversation_history,
        customer_context=customer_context,
    )

    # Save AI response
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_result["response"],
        tokens_used=ai_result.get("tokens_used", 0),
    )
    db.add(assistant_message)

    # Update conversation metadata
    conversation.intent_detected = ai_result.get("intent")
    conversation.context = {
        **(conversation.context or {}),
        "last_intent": ai_result.get("intent"),
        "suggested_actions": ai_result.get("suggested_actions", []),
    }

    await db.commit()
    await db.refresh(conversation)

    return ChatResponse(
        conversation_id=conversation.id,
        response=ai_result["response"],
        intent=ai_result.get("intent"),
        suggested_actions=ai_result.get("suggested_actions", []),
    )


@router.post("/sms/webhook", response_class=PlainTextResponse)
async def sms_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Webhook endpoint for incoming Twilio SMS messages.
    Processes the message with AI and returns TwiML response.
    """
    # Parse form data from Twilio
    form_data = await request.form()
    from_number = form_data.get("From", "")
    to_number = form_data.get("To", "")
    body = form_data.get("Body", "")
    message_sid = form_data.get("MessageSid", "")

    if not body:
        return twilio_service.create_response(
            "Hello! How can I help you with your property maintenance needs today?"
        )

    # Find or create customer by phone
    customer_result = await db.execute(
        select(Customer).where(Customer.phone == from_number)
    )
    customer = customer_result.scalar_one_or_none()

    # Find active conversation or create new one
    conv_result = await db.execute(
        select(Conversation)
        .where(
            Conversation.phone_number == from_number,
            Conversation.channel == "sms",
            Conversation.status == "active",
        )
        .order_by(Conversation.created_at.desc())
    )
    conversation = conv_result.scalar_one_or_none()

    conversation_history = []
    if conversation:
        # Load history
        messages_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
            .limit(10)  # Limit history for SMS context
        )
        for msg in messages_result.scalars().all():
            conversation_history.append({
                "role": msg.role,
                "content": msg.content,
            })
    else:
        # Create new conversation
        conversation = Conversation(
            customer_id=customer.id if customer else None,
            channel="sms",
            phone_number=from_number,
            external_id=message_sid,
            status="active",
        )
        db.add(conversation)
        await db.flush()

    # Save incoming message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=body,
        external_id=message_sid,
    )
    db.add(user_message)

    # Get customer context
    customer_context = None
    if customer:
        customer_context = {
            "name": customer.full_name,
            "address": customer.full_address,
        }

    # Get AI response
    ai_result = await ai_agent.chat(
        message=body,
        conversation_history=conversation_history,
        customer_context=customer_context,
    )

    # Save AI response
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_result["response"],
        tokens_used=ai_result.get("tokens_used", 0),
    )
    db.add(assistant_message)

    # Update conversation
    conversation.intent_detected = ai_result.get("intent")

    await db.commit()

    # Return TwiML response
    return twilio_service.create_response(ai_result["response"])


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a conversation with all messages."""
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Load messages
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    conversation.messages = messages_result.scalars().all()

    return conversation


@router.post("/{conversation_id}/close")
async def close_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Close a conversation."""
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    from datetime import datetime
    conversation.status = "closed"
    conversation.closed_at = datetime.utcnow()

    await db.commit()
    return {"status": "closed"}
