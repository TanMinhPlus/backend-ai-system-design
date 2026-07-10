from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["System design reading notes"],
    )
    content: str = Field(
        ...,
        min_length=1,
        examples=[
            "FastAPI handles API routing, PostgreSQL stores notes, and Groq powers AI summaries."
        ],
    )


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        examples=["What are the main backend components in this note?"],
    )


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    service: str


class ReadinessResponse(BaseModel):
    status: str
    database: str


class NoteSearchResponse(BaseModel):
    query: str
    count: int
    results: list[NoteRead]


class SummaryResponse(BaseModel):
    note_id: int
    summary: str


class AnswerResponse(BaseModel):
    note_id: int
    answer: str
