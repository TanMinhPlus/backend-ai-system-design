import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, init_db
from app.models import Note


DEMO_NOTES = [
    {
        "title": "Backend AI System Design",
        "content": (
            "The prototype uses FastAPI for REST endpoints, PostgreSQL for durable "
            "note storage, and Groq for AI summaries and note-based questions."
        ),
    },
    {
        "title": "Readiness checklist",
        "content": (
            "A stable prototype should expose health checks, typed API contracts, "
            "database migrations, useful docs, and repeatable tests."
        ),
    },
]


def seed_demo_notes() -> int:
    init_db()
    db = SessionLocal()
    created = 0
    try:
        for note in DEMO_NOTES:
            exists = db.query(Note).filter(Note.title == note["title"]).first()
            if exists:
                continue
            db.add(Note(**note))
            created += 1
        db.commit()
    finally:
        db.close()
    return created


if __name__ == "__main__":
    count = seed_demo_notes()
    print(f"Seeded {count} demo note(s).")
