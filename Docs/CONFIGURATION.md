# Configuration

All settings are loaded from environment variables (or `.env` in the project root) via `src/config/settings.py`.

## Environment variables

### OpenAI

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | API key (required for chat and embeddings) |
| `OPENAI_MODEL` | `gpt-4o` | Chat completion model |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model (1536 dimensions) |

### Pinecone

| Variable | Default | Description |
|----------|---------|-------------|
| `PINECONE_API_KEY` | — | API key (required for retrieval) |
| `PINECONE_INDEX_NAME` | `empowertech-rag` | Index name (must exist, dim 1536) |
| `PINECONE_NAMESPACE` | `default` | Namespace for vectors |

### PostgreSQL

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/empowertech_chatbot` | SQLAlchemy connection string |

**Docker Compose (API container):** use host `postgres` instead of `localhost`.

**Host scripts against compose Postgres:** use `localhost:5432`.

### Application

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `false` | Debug flag |
| `LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, …) |
| `CHAT_HISTORY_LIMIT` | `10` | Messages included in RAG prompt context |
| `RETRIEVAL_TOP_K` | `5` | Chunks retrieved per query |
| `RETRIEVAL_CONFIDENCE_THRESHOLD` | `0.3` | Below this score → guardrail fallback (no LLM) |
| `CORS_ORIGINS` | `""` | Comma-separated extra allowed origins |

`localhost:3000` and `127.0.0.1:3000` are always permitted for CORS regardless of `CORS_ORIGINS`.

### Frontend (build-time)

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000` | FastAPI base URL (no trailing slash) |
| `NEXT_PUBLIC_HIDE_COLD_START_HINT` | unset | Set `true` to hide Render cold-start banner |

`NEXT_PUBLIC_*` variables are baked in at **build** time. Rebuild/redeploy the frontend after changing them.

---

## Tuning retrieval quality

| Parameter | Effect |
|-----------|--------|
| `RETRIEVAL_TOP_K` | More chunks → broader context, higher token cost |
| `RETRIEVAL_CONFIDENCE_THRESHOLD` | Higher → stricter guardrails, more fallbacks |
| Ingestion `--chunk-size` / `--chunk-overlap` | Smaller chunks → finer retrieval; larger → more context per chunk |

Run `experiments/run_rag_evaluation.py` to compare `top_k` settings against `data/evaluation_gold.csv`.

---

## Example `.env` (local)

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

PINECONE_API_KEY=...
PINECONE_INDEX_NAME=empowertech-rag
PINECONE_NAMESPACE=default

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/empowertech_chatbot

LOG_LEVEL=INFO
CHAT_HISTORY_LIMIT=10
RETRIEVAL_TOP_K=5
RETRIEVAL_CONFIDENCE_THRESHOLD=0.3
```

Copy from `.env.example` at the repository root.
