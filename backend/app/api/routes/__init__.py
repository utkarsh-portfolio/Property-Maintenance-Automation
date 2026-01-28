from fastapi import APIRouter
from app.api.routes import customers, leads, appointments, conversations

api_router = APIRouter()

api_router.include_router(customers.router)
api_router.include_router(leads.router)
api_router.include_router(appointments.router)
api_router.include_router(conversations.router)
