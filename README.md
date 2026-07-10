# Backend AI System Design

> A FastAPI prototype for note management, search, and AI-assisted note analysis.

## Overview

This project demonstrates a backend service that stores notes, searches across them, summarizes note content, and answers note-specific questions through Groq's Llama model. It is structured as a practical prototype: typed API contracts, Swagger documentation, health checks, migrations, Docker Compose, demo seed data, and tests are included.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend Framework | FastAPI (Python) |
| Database | PostgreSQL 18 |
| ORM | SQLAlchemy + Alembic |
| AI Model | Llama 3.3 70B via Groq API |
| Containerization | Docker + Docker Compose |
| API Docs | Swagger UI + OpenAPI |
| Tests | Pytest + FastAPI TestClient |

## Features

- Full CRUD for notes
- Full-text search by title and content
- AI-powered note summarization
- AI-powered Q&A based on note content
- Standard HTTP error handling
- Docker ready

## Architecture

    Client (Swagger/Postman)
            ↓
       FastAPI App
            ↓
      Business Logic
        ↙        ↘
    PostgreSQL   Groq AI API
    (Data)       (Intelligence)

## Getting Started

### Requirements

- Python 3.11+
- Docker Desktop, if using PostgreSQL through Docker Compose
- Groq API key for AI endpoints

### Local Setup

    # 1. Clone repo
    git clone https://github.com/TanMinhPlus/backend-ai-system-design
    cd backend-ai-system-design

    # 2. Create virtual environment
    python -m venv venv
    venv\Scripts\activate

    # 3. Install dependencies
    pip install -r requirements.txt

    # 4. Create .env file
    cp .env.example .env

    # 5. Run server
    uvicorn app.main:app --reload

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

## API Documentation

After running the server, visit: **http://localhost:8000/docs**

## Author

**Pham Tan Minh** — Backend + AI Developer (Fresher)
- GitHub: [@TanMinhPlus](https://github.com/TanMinhPlus)
