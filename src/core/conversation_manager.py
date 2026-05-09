from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.database import ChatMessage, ChatSession, MessageRole, User


class ConversationManager:
    def _recalculate_session_avg_sentiment(self, db: Session, session: ChatSession) -> None:
        """Mean sentiment over user turns that have sentiment.score in metadata (VADER compound)."""
        q = (
            select(ChatMessage.message_metadata)
            .where(ChatMessage.session_id == session.id, ChatMessage.role == MessageRole.user)
            .order_by(ChatMessage.timestamp.asc())
        )
        scores: list[float] = []
        for meta in db.execute(q).scalars():
            if not meta or not isinstance(meta, dict):
                continue
            sent = meta.get("sentiment")
            if isinstance(sent, dict) and sent.get("score") is not None:
                try:
                    scores.append(float(sent["score"]))
                except (TypeError, ValueError):
                    pass
        session.avg_sentiment = sum(scores) / len(scores) if scores else None

    def get_or_create_user(self, db: Session, user_id: str, email: Optional[str] = None) -> User:
        user = db.execute(select(User).where(User.user_id == user_id)).scalar_one_or_none()
        if user:
            if email and user.email != email:
                user.email = email
            return user
        user = User(user_id=user_id, email=email)
        db.add(user)
        db.flush()
        return user

    def create_session(self, db: Session, user: User) -> ChatSession:
        s = ChatSession(session_id=str(uuid.uuid4()), user_id=user.id, start_time=datetime.utcnow())
        db.add(s)
        db.flush()
        return s

    def get_session(self, db: Session, session_id: str) -> Optional[ChatSession]:
        return db.execute(select(ChatSession).where(ChatSession.session_id == session_id)).scalar_one_or_none()

    def add_message(
        self,
        db: Session,
        session: ChatSession,
        role: MessageRole,
        content: str,
        intent: Optional[str] = None,
        confidence: Optional[float] = None,
        retrieved_context: Optional[Union[List[Any], Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tokens_used: Optional[int] = None,
    ) -> ChatMessage:
        m = ChatMessage(
            message_id=str(uuid.uuid4()),
            session_id=session.id,
            role=role,
            content=content,
            intent=intent,
            confidence=confidence,
            retrieved_context=retrieved_context,
            message_metadata=metadata,
            tokens_used=tokens_used,
        )
        db.add(m)
        session.message_count = (session.message_count or 0) + 1
        db.flush()
        self._recalculate_session_avg_sentiment(db, session)
        return m

    def load_history(self, db: Session, session: ChatSession, limit: int) -> List[Dict[str, Any]]:
        q = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session.id)
            .order_by(ChatMessage.timestamp.desc())
            .limit(limit)
        )
        rows = list(db.execute(q).scalars().all())
        rows.reverse()
        return [
            {"role": r.role.value, "content": r.content, "timestamp": r.timestamp.isoformat()} for r in rows
        ]

