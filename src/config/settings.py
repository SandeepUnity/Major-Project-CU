from __future__ import annotations

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"

    # Pinecone
    pinecone_api_key: Optional[str] = None
    pinecone_index_name: str = "empowertech-rag"
    pinecone_namespace: str = "default"

    # PostgreSQL
    database_url: str = "postgresql://postgres:postgres@localhost:5432/empowertech_chatbot"

    # App
    debug: bool = False
    log_level: str = "INFO"
    chat_history_limit: int = 10
    retrieval_top_k: int = 5
    retrieval_confidence_threshold: float = 0.3
    broad_topic_retrieval_confidence_threshold: float = 0.2

    # CORS: comma-separated origins (e.g. https://your-frontend.onrender.com). Local dev origins always allowed.
    cors_origins: str = ""


settings = Settings()

