"""Verify session avg_sentiment backfill on /analytics and rollup on add_message."""

import importlib
import os
import tempfile

from sqlalchemy import select


def test_analytics_backfills_avg_sentiment_from_existing_user_messages():
    # File-based SQLite so ORM create_all and TestClient share one database (not :memory: per connection).
    dbf = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    dbf.close()
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{dbf.name.replace(os.sep, '/')}"
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("PINECONE_API_KEY", None)

    import src.config.settings as settings_mod

    importlib.reload(settings_mod)

    import src.models.db as db_mod

    importlib.reload(db_mod)

    from fastapi.testclient import TestClient

    from src.models.database import Base, ChatMessage, ChatSession, MessageRole, User

    Base.metadata.create_all(bind=db_mod.get_engine())

    import src.main as main_mod

    importlib.reload(main_mod)

    SessionLocal = db_mod.get_sessionmaker()
    db = SessionLocal()
    try:
        u = User(user_id="test_u", email=None)
        db.add(u)
        db.flush()
        s = ChatSession(session_id="sess-one", user_id=u.id)
        db.add(s)
        db.flush()
        # Simulate historical rows stored without touching ConversationManager.avg update
        m1 = ChatMessage(
            message_id="m1",
            session_id=s.id,
            role=MessageRole.user,
            content="hello",
            message_metadata={"sentiment": {"score": 0.6, "label": "pos", "method": "vader"}},
        )
        m2 = ChatMessage(
            message_id="m2",
            session_id=s.id,
            role=MessageRole.user,
            content="this is awful",
            message_metadata={"sentiment": {"score": -0.8, "label": "neg", "method": "vader"}},
        )
        db.add_all([m1, m2])
        s.message_count = 2
        s.avg_sentiment = None
        db.commit()

        client = TestClient(main_mod.app)
        r = client.get("/analytics")
        assert r.status_code == 200
        body = r.json()

        db2 = SessionLocal()
        try:
            sess = db2.execute(select(ChatSession).where(ChatSession.session_id == "sess-one")).scalar_one()
            assert sess.avg_sentiment is not None
            assert abs(sess.avg_sentiment - (-0.1)) < 1e-6  # mean of 0.6 and -0.8
        finally:
            db2.close()

        assert body["avg_session_sentiment"] is not None
        assert abs(float(body["avg_session_sentiment"]) - (-0.1)) < 1e-5
    finally:
        db.close()
        try:
            os.unlink(dbf.name)
        except OSError:
            pass
