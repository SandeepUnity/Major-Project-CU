from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True, index=True)
    enrolled_courses: Mapped[Optional[Union[Dict[str, Any], List[Any]]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    sessions: Mapped[List["ChatSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    message_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_sentiment: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    handoff_triggered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    handoff_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship(back_populates="sessions")
    messages: Mapped[List["ChatMessage"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True)

    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole, name="message_role"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    intent: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    retrieved_context: Mapped[Optional[Union[Dict[str, Any], List[Any]]]] = mapped_column(JSON, nullable=True)
    message_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column("metadata", JSON, nullable=True)

    session: Mapped[ChatSession] = relationship(back_populates="messages")
    feedback: Mapped[Optional["Feedback"]] = relationship(back_populates="message", cascade="all, delete-orphan")


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = (UniqueConstraint("message_id", name="uq_feedback_message_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_messages.id"), nullable=False, index=True)

    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sentiment_label: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    user_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    ragas_faithfulness: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ragas_answer_relevancy: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ragas_context_recall: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ragas_average: Mapped[Optional[float]] = mapped_column(Float, nullable=True, index=True)

    chunking_size_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    retrieval_top_k: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    message: Mapped[ChatMessage] = relationship(back_populates="feedback")

