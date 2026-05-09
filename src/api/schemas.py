from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SessionCreateRequest(BaseModel):
    user_id: str = Field(..., examples=["user_1"])
    email: Optional[str] = Field(default=None, examples=["student@example.com"])


class SessionCreateResponse(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    query: str = Field(..., min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    response: str
    session_id: str
    confidence: Optional[float] = None
    handoff_trigger: bool
    intent: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HistoryResponse(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]]


class AnalyticsResponse(BaseModel):
    total_sessions: int
    total_messages: int
    avg_session_sentiment: Optional[float]
    handoff_rate: float


class HealthResponse(BaseModel):
    status: str
    dependencies: Dict[str, str]

