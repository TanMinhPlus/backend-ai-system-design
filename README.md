# Backend AI System Design

> A FastAPI prototype for note management, search, and AI-assisted note analysis.

## Overview

This project demonstrates a backend service that stores notes, searches across them, summarizes note content, and answers note-specific questions through Groq's Llama model. It is structured as a practical prototype: typed API contracts, Swagger documentation, health checks, migrations, Docker Compose, demo seed data, and tests are included.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend Framework | FastAPI (Python) |
| Database | PostgreSQL 16 via Docker Compose |
| ORM and Migrations | SQLAlchemy + Alembic |
| AI Model | Llama 3.3 70B via Groq API |
| Containerization | Docker + Docker Compose |
| API Docs | Swagger UI + OpenAPI |
| Tests | Pytest + FastAPI TestClient |

## Features

- Full CRUD for notes
- Search by title and content
- AI-powered note summarization
- AI-powered Q&A based on note content
- Health and readiness endpoints
- Typed request and response schemas
- Alembic migration scaffold
- Demo seed script
- Docker-ready PostgreSQL setup

## Architecture

```text
Client (Swagger/Postman)
        |
    FastAPI App
        |
  Route + Schema Layer
     /          \
SQLAlchemy     Groq API
PostgreSQL     Llama 3.3 70B
```

## Getting Started

### Requirements

- Python 3.11+
- Docker Desktop, if using PostgreSQL through Docker Compose
- Groq API key for AI endpoints

### Local Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Update `.env` with your own `GROQ_API_KEY`.

For a simple local prototype without PostgreSQL, you can use SQLite:

```text
DATABASE_URL=sqlite:///./backend_ai.db
```

Run the API:

```powershell
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

### Docker Setup

```powershell
docker compose up --build
```

The API runs at `http://localhost:8000` and PostgreSQL runs on port `5432`.

## Database Migrations

Run migrations with:

```powershell
alembic upgrade head
```

The app also supports `AUTO_CREATE_TABLES=true` for quick prototype startup. For a stricter migration-only workflow, set:

```text
AUTO_CREATE_TABLES=false
```

## Demo Data

Seed a couple of demo notes:

```powershell
python scripts/seed_demo.py
```

Then visit `/docs`, open `GET /notes`, and execute the request.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Basic API status |
| GET | `/health` | Liveness check |
| GET | `/ready` | Database readiness check |
| GET | `/notes` | List notes |
| POST | `/notes` | Create a note |
| GET | `/notes/search?q=` | Search notes |
| PUT | `/notes/{note_id}` | Update a note |
| DELETE | `/notes/{note_id}` | Delete a note |
| GET | `/notes/{note_id}/summarize` | Summarize note content |
| POST | `/notes/{note_id}/ask` | Ask a question about note content |

## Test

```powershell
pytest
```

The tests use an in-memory SQLite database and mock the AI behavior where needed, so they do not call Groq.

## Prototype Notes

This is now a proper backend prototype rather than only a skeleton. The main remaining upgrade for production would be replacing prototype auto-table creation with a migration-only deploy process, adding authentication, adding request rate limits, and introducing structured logging/observability.

## Author

**Pham Tan Minh** - Backend + AI Developer (Fresher)

GitHub: [@TanMinhPlus](https://github.com/TanMinhPlus)
