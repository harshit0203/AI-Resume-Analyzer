# AIResumeAnalyzer

A production-grade, full-stack SaaS that analyzes resumes with a **multi-agent AI workflow**. Upload a PDF/DOCX resume and six specialized agents (built on **LangGraph + LangChain**) score ATS compatibility, find skill gaps, match jobs, rewrite weak content and coach your career — streamed live over WebSockets.

- **Frontend:** Next.js 16 (App Router) · TypeScript · Tailwind CSS v4 · shadcn-style UI · Framer Motion · TanStack Query · Zustand · React Hook Form · Zod · Recharts
- **Backend:** FastAPI · SQLAlchemy 2 (async) · PostgreSQL · Alembic · Redis · LangGraph · LangChain · OpenAI
- **Auth:** JWT access + refresh tokens in **httpOnly secure cookies**, bcrypt hashing, role management, edge route protection

---

## Table of contents

1. [Architecture](#architecture)
2. [Project structure](#project-structure)
3. [The multi-agent workflow](#the-multi-agent-workflow)
4. [Database schema](#database-schema)
5. [Authentication & security](#authentication--security)
6. [Local development](#local-development)
7. [Running with Docker](#running-with-docker)
8. [API overview](#api-overview)
9. [Environment variables](#environment-variables)
10. [Production & deployment](#production--deployment)

---

## Architecture

```
┌─────────────────────────────┐         ┌──────────────────────────────────────┐
│         Next.js 16          │  HTTPS  │               FastAPI                  │
│  App Router · RSC · TS      │ ──────▶ │  Routers → Services → Repositories     │
│  TanStack Query · Zustand   │ ◀────── │  Pydantic schemas · DI · middleware    │
│  Tailwind v4 · Framer       │  WS     │                                        │
└─────────────┬───────────────┘         └───────────────┬───────────────────────┘
              │ httpOnly cookies                          │
              │                              ┌────────────┼───────────────┐
              │                              ▼            ▼               ▼
              │                        PostgreSQL      Redis        LangGraph
              │                       (SQLAlchemy)   (cache/RL)    6-agent graph
              │                                                         │
              └──────────── live agent updates ◀── WebSocket ───────────┘
```

**Layered backend (clean architecture / DDD):**

`API (routers)` → `Services (use-cases)` → `Repositories (data access)` → `Models (domain)`, with `Schemas` (Pydantic) at the boundaries and cross-cutting `core` concerns (config, logging, security, middleware).

---

## Project structure

```
AIResumeAnalyzer/
├── backend/
│   ├── app/
│   │   ├── core/          # config, logging, security, db, redis, exceptions, middleware
│   │   ├── models/        # SQLAlchemy models (User, Resume, Analysis, …)
│   │   ├── schemas/       # Pydantic request/response models
│   │   ├── repositories/  # async data-access layer
│   │   ├── services/      # business logic (auth, resume, analysis, storage, realtime)
│   │   ├── agents/        # LangGraph workflow + 6 AI agents + deterministic engine
│   │   ├── api/           # deps, cookies, v1 routers & endpoints, websocket
│   │   └── main.py        # FastAPI app factory
│   ├── alembic/           # migrations (async env)
│   ├── scripts/           # create_tables bootstrap
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── app/               # routes: landing, (auth), dashboard/*
│   ├── components/        # ui/ (shadcn-style), marketing/, dashboard/, charts/
│   ├── lib/               # api client, types, hooks, stores, utils, motion
│   ├── proxy.ts           # edge route protection
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md
```

---

## The multi-agent workflow

A compiled **LangGraph** `StateGraph` runs agents sequentially, sharing typed state and emitting lifecycle events:

```
START → Resume Parser → ATS Analyzer → Skill Gap → Job Match → Resume Improvement → Career Coach → END
```

| Agent | Output |
|-------|--------|
| **Resume Parser** | name, email, phone, skills, education, certifications, projects, experience |
| **ATS Analyzer** | ATS score, strengths, weaknesses, missing keywords, recommendations |
| **Skill Gap** | matched/missing skills vs. a career path + learning roadmap |
| **Job Match** | top roles with match %, reasons, matched & missing skills |
| **Resume Improvement** | stronger summary, rewritten bullets, ATS keywords |
| **Career Coach** | salary insights, next steps, certifications, growth roadmap |

> **Works without an API key.** Each agent uses OpenAI (via LangChain) when `OPENAI_API_KEY` is set, and falls back to a deterministic, rule-based engine otherwise — so the product is fully functional out of the box. Every step is streamed to the client via WebSocket (`/ws/analyses/{id}`) and persisted as an `AgentExecution` for the dashboard timeline.

---

## Database schema

| Table | Purpose | Key relationships |
|-------|---------|-------------------|
| `users` | accounts, role, plan | → resumes, analyses, settings |
| `user_settings` | preferences & notifications | 1–1 user |
| `resumes` | uploaded files + parsed JSON, versioning | → analyses |
| `analyses` | a full multi-agent run, scores, status | → agent_executions, job_matches, career_insight |
| `agent_executions` | per-agent status/output/timing | n–1 analysis |
| `job_matches` | matched roles with scores | n–1 analysis |
| `career_insights` | coaching output | 1–1 analysis |

All tables use UUID primary keys and timezone-aware `created_at` / `updated_at`. JSONB columns store flexible AI outputs.

---

## Authentication & security

- **JWT** access (short-lived) + refresh (long-lived) tokens, signed with separate secrets.
- Tokens are delivered as **httpOnly, SameSite, Secure** cookies — never exposed to JS (XSS-safe). The access token is also returned in the login/register body for header-based API clients.
- The Axios client auto-refreshes on `401` and retries once; the Next.js edge `proxy` gates `/dashboard/*`.
- **bcrypt** password hashing, password-strength validation, login-enumeration mitigation.
- CORS allowlist, security headers, request IDs, structured rotating logs, and **rate limiting** (SlowAPI/Redis).
- File uploads are validated by extension, size and content; stored per-user.

---

## Local development

### Prerequisites
- Node.js 20+, Python 3.12+, PostgreSQL 14+, Redis 6+ (Redis optional in dev)

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate        # macOS/Linux
pip install -r requirements.txt

copy .env.example .env            # then fill in values (see below)

# Create the schema (dev bootstrap) …
python -m scripts.create_tables
# … or use migrations:
# alembic revision --autogenerate -m "init"
# alembic upgrade head

uvicorn app.main:app --reload
```

API: http://localhost:8000 · Docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
copy .env.example .env.local      # set NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

App: http://localhost:3000

---

## Running with Docker

```bash
cp .env.example .env              # set POSTGRES_USER/PASSWORD/DB
cp backend/.env.example backend/.env   # fill backend secrets (OPENAI_API_KEY optional)
docker compose up --build
```

This starts PostgreSQL, Redis, the FastAPI backend (auto-creates tables) and the Next.js frontend.

- Frontend → http://localhost:3000
- Backend  → http://localhost:8000/docs

---

## API overview

Base path: `/api/v1` · Consistent envelopes: `{ success, data, message }` and paginated `{ items, meta }`.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Create account, set cookies |
| POST | `/auth/login` | Authenticate, set cookies |
| POST | `/auth/refresh` | Rotate access token |
| POST | `/auth/logout` | Clear cookies |
| GET | `/auth/me` | Current user |
| GET/PATCH | `/users/me` | Profile |
| POST | `/users/me/change-password` | Change password |
| GET/PATCH | `/users/me/settings` | Preferences |
| POST/GET | `/resumes` | Upload / list resumes |
| GET/DELETE | `/resumes/{id}` | Retrieve / delete |
| GET | `/resumes/{id}/download` | Download original |
| POST | `/resumes/{id}/primary` | Set primary |
| POST/GET | `/analyses` | Start / list analyses |
| GET | `/analyses/stats` | Aggregate stats |
| GET/DELETE | `/analyses/{id}` | Detail / delete |
| WS | `/ws/analyses/{id}` | Live agent updates |

---

## Environment variables

See [`backend/.env.example`](backend/.env.example) and [`frontend/.env.example`](frontend/.env.example) for the full list (PostgreSQL URL, Redis URL, OpenAI key, JWT secrets, cookie config, frontend/backend URLs, storage, rate limits).

---

## Production & deployment

- **Containers:** multi-stage Dockerfiles for both apps; orchestrate with the provided `docker-compose.yml` or any container platform (ECS, Cloud Run, Fly, Render, Kubernetes).
- **Migrations:** run `alembic upgrade head` on deploy (the compose backend bootstraps tables for convenience).
- **Secrets:** set strong `JWT_SECRET_KEY` / `JWT_REFRESH_SECRET_KEY`, `COOKIE_SECURE=true`, `ENVIRONMENT=production`, and a locked-down `CORS_ORIGINS`.
- **Scalability:** the API is stateless (scale horizontally behind a load balancer); Postgres + Redis are the shared state. Long-running analyses run as background tasks and stream via WebSocket — move to a Celery/RQ worker for very high throughput.
- **Observability:** structured JSON logs with rotation (`logs/app.log`, `logs/error.log`) and per-request IDs are emitted out of the box.

---

Built with Next.js, FastAPI & LangGraph.
