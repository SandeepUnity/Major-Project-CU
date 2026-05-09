from __future__ import annotations

import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.api.schemas import (
    AnalyticsResponse,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    HistoryResponse,
    SessionCreateRequest,
    SessionCreateResponse,
)
from src.config.settings import settings
from src.core.chat_orchestrator import ChatOrchestrator
from src.core.conversation_manager import ConversationManager
from src.models.database import ChatMessage, ChatSession
from src.models.db import get_db
from src.utils.logger import configure_logging

configure_logging(settings.log_level)
logger = logging.getLogger("app")


def _allowed_cors_origins() -> list[str]:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    extra = (getattr(settings, "cors_origins", None) or "").strip()
    for part in extra.split(","):
        p = part.strip()
        if p and p not in origins:
            origins.append(p)
    return origins


app = FastAPI(title="EmpowerTech RAG Chatbot", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = ChatOrchestrator()
conv = ConversationManager()


@app.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)):
    deps: dict[str, str] = {"postgres": "unknown", "openai": "unknown", "pinecone": "unknown"}
    try:
        db.execute(select(func.now()))
        deps["postgres"] = "ok"
    except Exception as e:  # pragma: no cover
        deps["postgres"] = f"error: {e.__class__.__name__}"
    deps["openai"] = "configured" if bool(settings.openai_api_key) else "not_configured"
    deps["pinecone"] = "configured" if bool(settings.pinecone_api_key) else "not_configured"
    status = "healthy" if deps["postgres"] == "ok" else "degraded"
    return HealthResponse(status=status, dependencies=deps)


@app.post("/session", response_model=SessionCreateResponse)
def create_session(payload: SessionCreateRequest, db: Session = Depends(get_db)):
    user = conv.get_or_create_user(db, user_id=payload.user_id, email=payload.email)
    session = conv.create_session(db, user)
    db.commit()
    return SessionCreateResponse(session_id=session.session_id)


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        result = orchestrator.chat(db, user_id=payload.user_id, session_id=payload.session_id, query=payload.query)
        return ChatResponse(
            response=result.response,
            session_id=result.session_id,
            confidence=result.confidence,
            handoff_trigger=result.handoff_trigger,
            intent=result.intent,
            metadata=result.metadata,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:  # pragma: no cover
        logger.exception("chat failed")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@app.get("/history", response_model=HistoryResponse)
def history(session_id: str, db: Session = Depends(get_db)):
    session = conv.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    msgs = conv.load_history(db, session, limit=200)
    return HistoryResponse(session_id=session_id, messages=msgs)


@app.get("/analytics", response_model=AnalyticsResponse)
def analytics(db: Session = Depends(get_db)):
    # Backfill per-session averages from stored user-message metadata (historical rows pre-fix)
    for sess in db.execute(select(ChatSession).where(ChatSession.avg_sentiment.is_(None))).scalars().all():
        conv._recalculate_session_avg_sentiment(db, sess)
    db.commit()

    total_sessions = db.execute(select(func.count()).select_from(ChatSession)).scalar_one()
    total_messages = db.execute(select(func.count()).select_from(ChatMessage)).scalar_one()

    avg_sent = db.execute(select(func.avg(ChatSession.avg_sentiment))).scalar_one()
    handoff_count = db.execute(select(func.count()).select_from(ChatSession).where(ChatSession.handoff_triggered.is_(True))).scalar_one()
    handoff_rate = float(handoff_count) / float(total_sessions) if total_sessions else 0.0

    return AnalyticsResponse(
        total_sessions=int(total_sessions),
        total_messages=int(total_messages),
        avg_session_sentiment=float(avg_sent) if avg_sent is not None else None,
        handoff_rate=handoff_rate,
    )

