# Property Maintenance Automation

AI-powered property maintenance scheduling and lead management system. Built to demonstrate skills relevant for a **Forward Deployed Engineer** role at Revin AI.

## Features

- **AI Conversation Agent** - Natural language chatbot for scheduling, inquiries, and lead qualification
- **Lead Management** - Track and convert leads with status tracking and follow-ups
- **Appointment Scheduling** - Full scheduling system with conflict detection and reminders
- **SMS Integration** - Twilio-powered SMS for appointment reminders and customer communication
- **Customer Management** - Complete CRM functionality for property owners
- **Analytics Dashboard** - Real-time metrics on leads, conversions, and revenue

## Tech Stack

### Backend (Python)
- **FastAPI** - Modern async Python web framework
- **SQLAlchemy** - Async ORM for PostgreSQL
- **Groq** - Free LLM API (Llama 3.1)
- **Twilio** - SMS/Voice integration
- **Pydantic** - Data validation

### Frontend (TypeScript)
- **Next.js 14** - React framework with App Router
- **Tailwind CSS** - Utility-first styling
- **Lucide Icons** - Beautiful icon set
- **Recharts** - Data visualization

### Infrastructure (Free Tier)
- **Neon** - Serverless PostgreSQL
- **Upstash** - Serverless Redis
- **Vercel** - Frontend hosting
- **Render** - Backend hosting

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL (or use Docker)

### 1. Clone and Setup

```bash
git clone <repo-url>
cd Property-Maintenance-Automation
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 4. Using Docker (Alternative)

```bash
# Development mode with hot reload
docker-compose -f docker-compose.dev.yml up

# Production mode
docker-compose up --build
```

## Free API Keys Setup

### Groq (AI/LLM) - Required
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Create an API key
4. Add to `.env`: `GROQ_API_KEY=your_key`

### Twilio (SMS) - Optional
1. Go to [twilio.com/console](https://twilio.com/console)
2. Sign up for free trial ($15 credit)
3. Get your Account SID, Auth Token, and phone number
4. Add to `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

### Neon (Database) - For Production
1. Go to [neon.tech](https://neon.tech)
2. Create a free project
3. Copy the connection string
4. Add to `.env`: `DATABASE_URL=postgresql+asyncpg://...`

## Free Deployment

### Option 1: Render (Recommended)

1. Fork this repo to your GitHub
2. Go to [render.com](https://render.com)
3. Click "New" > "Blueprint"
4. Connect your GitHub repo
5. Render will auto-detect `render.yaml` and deploy everything

### Option 2: Vercel + Render

**Frontend on Vercel:**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repo
3. Set root directory to `frontend`
4. Add environment variable: `API_URL=your-render-backend-url`

**Backend on Render:**
1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your repo, set root to `backend`
4. Add environment variables from `.env`

### Option 3: Railway

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub
3. Add PostgreSQL and Redis services
4. Configure environment variables

## Project Structure

```
Property-Maintenance-Automation/
├── backend/                    # Python FastAPI
│   ├── app/
│   │   ├── api/routes/        # API endpoints
│   │   ├── core/              # Config, database
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   │   ├── ai_agent.py    # AI conversation agent
│   │   │   └── twilio_service.py
│   │   └── main.py            # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                   # Next.js
│   ├── app/                   # App router pages
│   │   ├── dashboard/
│   │   ├── leads/
│   │   ├── appointments/
│   │   ├── chat/              # AI chat interface
│   │   └── settings/
│   ├── components/            # React components
│   ├── lib/                   # Utilities, API client
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml         # Production
├── docker-compose.dev.yml     # Development
├── render.yaml                # Render deployment
└── README.md
```

## API Endpoints

### Customers
- `GET /api/v1/customers` - List customers
- `POST /api/v1/customers` - Create customer
- `GET /api/v1/customers/{id}` - Get customer
- `PATCH /api/v1/customers/{id}` - Update customer

### Leads
- `GET /api/v1/leads` - List leads
- `GET /api/v1/leads/stats` - Lead statistics
- `POST /api/v1/leads` - Create lead
- `PATCH /api/v1/leads/{id}` - Update lead

### Appointments
- `GET /api/v1/appointments` - List appointments
- `GET /api/v1/appointments/today` - Today's appointments
- `POST /api/v1/appointments` - Create appointment
- `POST /api/v1/appointments/{id}/confirm` - Confirm appointment

### Conversations (AI Chat)
- `POST /api/v1/conversations/chat` - Send message to AI
- `POST /api/v1/conversations/sms/webhook` - Twilio webhook
- `GET /api/v1/conversations/{id}` - Get conversation

## Why This Project?

This project demonstrates key skills for a **Forward Deployed Engineer** at Revin AI:

1. **Domain Relevance** - Built for home services industry (Revin's focus)
2. **AI Integration** - Conversational AI for customer service automation
3. **Full-Stack Development** - End-to-end implementation
4. **API Integrations** - CRM-like functionality, Twilio for communications
5. **Production-Ready** - Docker, deployment configs, proper architecture

## License

MIT
