# RouteX – Bus Ticket Booking Platform

RouteX is a production-oriented, full-stack bus ticket booking platform inspired by RedBus. It bridges customers, bus operators, and platform administrators with real-time seat locks, Razorpay payment verification, background jobs, and WebSocket-driven operator communication.

---

## Architecture Overview

RouteX is architected using **Clean Architecture** principles, enforcing separation of concerns across distinct layers:

```
GoRoute/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI routers & endpoint handlers (HTTP / WS layer)
│   │   │   └── v1/          # Versioned API routes (health, auth, buses, bookings, etc.)
│   │   ├── core/            # App settings (Pydantic), DB engine, security helpers
│   │   ├── models/          # SQLAlchemy 2.0 ORM database models
│   │   ├── schemas/         # Pydantic v2 data validation and serialization schemas
│   │   ├── services/        # Business logic layer (orchestrates transactions, payments, locks)
│   │   ├── repositories/    # Database query abstraction layer (CRUD operations)
│   │   └── main.py          # Application entrypoint & middleware configuration
│   ├── alembic/             # Asynchronous database migration scripts
│   ├── tests/               # Pytest async unit and integration tests
│   ├── requirements.txt     # Python dependencies
│   └── pytest.ini           # Test runner configuration
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Route views (Customer search, Seat booking, Operator dashboard)
│   │   ├── services/        # Axios API client and network calls
│   │   ├── hooks/           # Custom React hooks
│   │   ├── App.jsx          # Main application component & routes
│   │   └── main.jsx         # React DOM mounting
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── docker-compose.yml       # PostgreSQL 16 & Redis 7 services
└── README.md
```

---

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 (async), asyncpg, Alembic, Pydantic v2
- **Frontend**: React 18, Vite, Tailwind CSS, Axios, Lucide Icons
- **Data & Caching**: PostgreSQL 16, Redis 7 (for distributed seat reservation locks)
- **Asynchronous Tasks**: Celery (notifications and departure reminders)
- **Real-Time**: WebSockets for passenger-operator communications

---

## Getting Started

### 1. Prerequisites
- Python 3.12+
- Node.js 18+ and npm
- PostgreSQL 16 & Redis (via Docker Compose or local installation)

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables in `backend/.env` (refer to `.env.example`).
5. Run migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Interactive Swagger documentation is available at: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   Access the frontend application at: [http://localhost:5173](http://localhost:5173)

### 4. Running Tests
Run unit and integration tests using Pytest:
```bash
cd backend
.venv/bin/pytest -v
```

---

## Development Milestones

- [x] **Milestone 1**: Scaffolding & Environment Setup
  - FastAPI asynchronous database engine & session dependency
  - PostgreSQL connectivity & Alembic async configuration
  - Health check endpoint (`/api/v1/health`)
  - React + Vite + Tailwind CSS scaffolding with live status integration
  - Automated Pytest test suite for health and root endpoints
- [ ] **Milestone 2**: Authentication & Role-Based Access Control (RBAC)
  - SQLAlchemy models for Users (Customer, Operator, Super Admin)
  - Password hashing with Bcrypt/Argon2
  - JWT token generation (Access & Refresh tokens) and authentication dependencies
  - Registration & login endpoints + React login/register UI
- [ ] **Milestone 3**: Bus, Route, and Trip Scheduling
  - Bus layouts (Seater, Sleeper, Upper/Lower berths)
  - Routes, intermediate stops, and pricing matrix
  - Operator dashboard for fleet and schedule management
- [ ] **Milestone 4**: Bus Search & Interactive Seat Booking
  - Search buses by origin, destination, and travel date
  - Interactive SVG/Canvas seat layout visualizer
  - Redis distributed seat locks with 10-minute expiration
- [ ] **Milestone 5**: Razorpay Payment Integration & Double-Booking Prevention
  - Order creation and backend signature verification
  - Idempotent webhook processing
  - Atomic database transactions with row-level locks
- [ ] **Milestone 6**: Celery Background Jobs & Departure Notifications
  - Email confirmation upon booking
  - Automated 24-hour departure reminders
- [ ] **Milestone 7**: Real-time Passenger-Operator WebSockets Chat
  - Authorized WebSocket endpoints active within 24h of departure
  - Message persistence in PostgreSQL
