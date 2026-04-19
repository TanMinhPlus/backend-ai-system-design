from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db, engine
from app import models
from app.ai import summarize_note, ask_about_note

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend AI System Design")

class NoteCreate(BaseModel):
    title: str
    content: str

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes

@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"message": f"Note {note_id} deleted successfully"}

@app.get("/notes/{note_id}/summarize")
def summarize(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    summary = summarize_note(db_note.content)
    return {"note_id": note_id, "summary": summary}

@app.post("/notes/{note_id}/ask")
def ask(note_id: int, req: QuestionRequest, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    answer = ask_about_note(db_note.content, req.question)
    return {"note_id": note_id, "answer": answer}