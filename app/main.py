from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db, engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend AI System Design")

class NoteCreate(BaseModel):
    title: str
    content: str

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