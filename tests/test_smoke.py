import importlib
import os


def test_app_import_and_health():
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("PINECONE_API_KEY", None)

    import src.config.settings as settings_mod

    importlib.reload(settings_mod)

    import src.models.db as db_mod

    importlib.reload(db_mod)

    from fastapi.testclient import TestClient

    from src.models.database import Base
    from src.models.db import get_engine

    Base.metadata.create_all(bind=get_engine())

    import src.main as main_mod

    importlib.reload(main_mod)

    client = TestClient(main_mod.app)
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body
    assert "dependencies" in body

