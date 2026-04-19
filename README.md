# 🚀 Backend AI System Design

> A smart REST API integrated with AI for note management and analysis

## 📋 Overview

A production-ready backend REST API that leverages AI to summarize content and answer questions based on notes. Built following Backend + AI + System Design principles.

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend Framework | FastAPI (Python) |
| Database | PostgreSQL 18 |
| ORM | SQLAlchemy + Alembic |
| AI Model | Llama 3.3 70B via Groq API |
| Containerization | Docker + Docker Compose |
| API Docs | Swagger UI (built-in) |

## ✨ Features

- ✅ Full CRUD for notes
- ✅ Full-text search by title and content
- ✅ AI-powered note summarization
- ✅ AI-powered Q&A based on note content
- ✅ Standard HTTP error handling
- ✅ Docker ready

## 🏗 Architecture

    Client (Swagger/Postman)
            ↓
       FastAPI App
            ↓
      Business Logic
        ↙        ↘
    PostgreSQL   Groq AI API
    (Data)       (Intelligence)

## 🚀 Getting Started

### Requirements
- Python 3.11+
- PostgreSQL
- Docker (optional)

### Setup

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

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| GET | /notes | Get all notes |
| POST | /notes | Create a new note |
| GET | /notes/search?q= | Search notes |
| PUT | /notes/{id} | Update a note |
| DELETE | /notes/{id} | Delete a note |
| GET | /notes/{id}/summarize | AI summarize note |
| POST | /notes/{id}/ask | AI answer question |

## 📖 API Documentation

After running the server, visit: **http://localhost:8000/docs**

## 👨‍💻 Author

**Pham Tan Minh** — Backend + AI Developer
- GitHub: [@TanMinhPlus](https://github.com/TanMinhPlus)