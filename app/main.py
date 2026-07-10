import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app.ai import summarize_note, ask_about_note
from app.database import check_database, get_db, init_db
from app.schemas import (
    AnswerResponse,
    HealthResponse,
    MessageResponse,
    NoteCreate,
    NoteRead,
    NoteSearchResponse,
    QuestionRequest,
    ReadinessResponse,
    SummaryResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("AUTO_CREATE_TABLES", "true").lower() == "true":
        init_db()
    yield


tags_metadata = [
    {
        "name": "Health",
        "description": "Operational checks for uptime monitors and deployment readiness.",
    },
    {
        "name": "Notes",
        "description": "CRUD and search operations for saved notes.",
    },
    {
        "name": "AI",
        "description": "Groq-powered summarization and Q&A over note content.",
    },
]


app = FastAPI(
    title="Backend AI System Design",
    summary="AI-assisted note management API",
    description=(
        "A prototype FastAPI backend that combines note CRUD, search, "
        "PostgreSQL persistence, and Groq-powered AI analysis."
    ),
    version="0.2.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)


@app.get("/", response_model=MessageResponse, tags=["Health"], summary="API status")
def root():
    return {"message": "Backend AI System Design API is running"}


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Liveness check",
)
def health():
    return {"status": "ok", "service": "backend-ai-system-design"}


@app.get(
    "/ready",
    response_model=ReadinessResponse,
    tags=["Health"],
    summary="Database readiness check",
)
def ready():
    try:
        check_database()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")
    return {"status": "ready", "database": "connected"}


@app.post(
    "/notes",
    response_model=NoteRead,
    tags=["Notes"],
    status_code=201,
    summary="Create a note",
)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.get(
    "/notes",
    response_model=list[NoteRead],
    tags=["Notes"],
    summary="List notes",
)
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).order_by(models.Note.id).all()
    return notes


@app.get(
    "/notes/search",
    response_model=NoteSearchResponse,
    tags=["Notes"],
    summary="Search notes",
)
def search_notes(
    q: str = Query(..., min_length=1, description="Search text for title or content"),
    db: Session = Depends(get_db),
):
    query = q.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    results = (
        db.query(models.Note)
        .filter(
            models.Note.title.ilike(f"%{query}%")
            | models.Note.content.ilike(f"%{query}%")
        )
        .order_by(models.Note.id)
        .all()
    )
    return {"query": query, "results": results, "count": len(results)}


@app.put(
    "/notes/{note_id}",
    response_model=NoteRead,
    tags=["Notes"],
    summary="Update a note",
)
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note


@app.delete(
    "/notes/{note_id}",
    response_model=MessageResponse,
    tags=["Notes"],
    summary="Delete a note",
)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"message": f"Note {note_id} deleted successfully"}


@app.get(
    "/notes/{note_id}/summarize",
    response_model=SummaryResponse,
    tags=["AI"],
    summary="Summarize a note",
)
def summarize(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    try:
        summary = summarize_note(db_note.content)
        return {"note_id": note_id, "summary": summary}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post(
    "/notes/{note_id}/ask",
    response_model=AnswerResponse,
    tags=["AI"],
    summary="Ask a question about a note",
)
def ask(note_id: int, req: QuestionRequest, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    try:
        answer = ask_about_note(db_note.content, req.question)
        return {"note_id": note_id, "answer": answer}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
