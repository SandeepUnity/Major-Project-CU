from __future__ import annotations

import uuid
from datetime import datetime, timedelta

from sqlalchemy import select

from src.models.database import ChatMessage, ChatSession, Feedback, MessageRole, User
from src.models.db import get_sessionmaker


def main() -> None:
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        existing = db.execute(select(User).limit(1)).scalar_one_or_none()
        if existing:
            print("Seed skipped (users already exist).")
            return

        users: list[User] = []
        for i in range(1, 6):
            users.append(
                User(
                    user_id=f"user_{i}",
                    email=None,  # privacy-first: optional
                    enrolled_courses=[f"course_{(i % 3) + 1}"],
                )
            )
        db.add_all(users)
        db.flush()

        sessions: list[ChatSession] = []
        for i in range(1, 11):
            u = users[i % len(users)]
            sessions.append(ChatSession(session_id=str(uuid.uuid4()), user_id=u.id))
        db.add_all(sessions)
        db.flush()

        now = datetime.utcnow()
        messages: list[ChatMessage] = []
        for s in sessions:
            for j in range(5):
                mid_user = str(uuid.uuid4())
                mid_assistant = str(uuid.uuid4())
                messages.append(
                    ChatMessage(
                        message_id=mid_user,
                        session_id=s.id,
                        role=MessageRole.user,
                        content=f"Sample question {j+1} for session {s.session_id}?",
                        timestamp=now - timedelta(minutes=10 - j),
                    )
                )
                messages.append(
                    ChatMessage(
                        message_id=mid_assistant,
                        session_id=s.id,
                        role=MessageRole.assistant,
                        content=f"Sample answer {j+1}.",
                        timestamp=now - timedelta(minutes=10 - j) + timedelta(seconds=2),
                        retrieved_context=[{"source_id": "seed", "score": 1.0, "text": "seed"}],
                        message_metadata={"source_ids": ["seed"], "top_k": 1},
                    )
                )
        db.add_all(messages)
        db.flush()

        # Add feedback for assistant messages only
        feedback: list[Feedback] = []
        for m in messages:
            if m.role != MessageRole.assistant:
                continue
            feedback.append(
                Feedback(
                    message_id=m.id,
                    sentiment_score=0.0,
                    sentiment_label="neutral",
                    ragas_faithfulness=None,
                    ragas_answer_relevancy=None,
                    ragas_context_recall=None,
                    ragas_average=None,
                    chunking_size_used=512,
                    retrieval_top_k=5,
                )
            )
        db.add_all(feedback)
        db.commit()
        print("Seed completed.")
    finally:
        db.close()


if __name__ == "__main__":
    main()

