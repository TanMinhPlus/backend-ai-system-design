import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["AUTO_CREATE_TABLES"] = "true"
os.environ["GROQ_API_KEY"] = "your_groq_key_here"

from fastapi.testclient import TestClient

from app.main import app


def test_health_and_ready():
    with TestClient(app) as client:
        health = client.get("/health")
        ready = client.get("/ready")

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert ready.status_code == 200
    assert ready.json()["database"] == "connected"


def test_note_crud_and_search():
    with TestClient(app) as client:
        created = client.post(
            "/notes",
            json={
                "title": "Prototype Note",
                "content": "FastAPI backend with AI summaries and search.",
            },
        )
        assert created.status_code == 201
        note_id = created.json()["id"]

        listed = client.get("/notes")
        assert listed.status_code == 200
        assert any(note["title"] == "Prototype Note" for note in listed.json())

        searched = client.get("/notes/search", params={"q": "AI"})
        assert searched.status_code == 200
        assert searched.json()["count"] == 1

        updated = client.put(
            f"/notes/{note_id}",
            json={
                "title": "Updated Note",
                "content": "Search and AI are covered by the API contract.",
            },
        )
        assert updated.status_code == 200
        assert updated.json()["title"] == "Updated Note"

        deleted = client.delete(f"/notes/{note_id}")
        assert deleted.status_code == 200
        assert "deleted successfully" in deleted.json()["message"]


def test_search_rejects_blank_query():
    with TestClient(app) as client:
        response = client.get("/notes/search", params={"q": "   "})

    assert response.status_code == 400
    assert response.json()["detail"] == "Query cannot be empty"


def test_missing_note_returns_404():
    with TestClient(app) as client:
        response = client.delete("/notes/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_ai_endpoints_can_be_exercised(monkeypatch):
    def fake_summary(content: str) -> str:
        assert "AI summaries" in content
        return "A short summary."

    def fake_answer(content: str, question: str) -> str:
        assert "AI summaries" in content
        assert question == "What does this note cover?"
        return "It covers backend AI summaries."

    monkeypatch.setattr("app.main.summarize_note", fake_summary)
    monkeypatch.setattr("app.main.ask_about_note", fake_answer)

    with TestClient(app) as client:
        created = client.post(
            "/notes",
            json={
                "title": "AI Note",
                "content": "This note covers AI summaries for backend notes.",
            },
        )
        note_id = created.json()["id"]

        summary = client.get(f"/notes/{note_id}/summarize")
        answer = client.post(
            f"/notes/{note_id}/ask",
            json={"question": "What does this note cover?"},
        )

    assert summary.status_code == 200
    assert summary.json()["summary"] == "A short summary."
    assert answer.status_code == 200
    assert answer.json()["answer"] == "It covers backend AI summaries."


def test_ai_configuration_error_is_reported(monkeypatch):
    from app.ai import get_groq_client

    get_groq_client.cache_clear()

    monkeypatch.setenv("GROQ_API_KEY", "your_groq_key_here")

    with TestClient(app) as client:
        created = client.post(
            "/notes",
            json={
                "title": "No AI Config",
                "content": "AI should fail cleanly.",
            },
        )

        assert created.status_code == 201
        note_id = created.json()["id"]

        response = client.get(
            f"/notes/{note_id}/summarize",
        )

    assert response.status_code == 503
    assert response.json()["detail"] == "GROQ_API_KEY is not configured"

    get_groq_client.cache_clear()
