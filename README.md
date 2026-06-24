# EmpowerTech RAG Chatbot (MSc Data Science Major Project)

Production-grade **Retrieval-Augmented Generation (RAG)** chatbot for EmpowerTech Solutions, an online education platform. The system provides 24/7 student support and produces **thesis-ready analytics** (RAG quality metrics, sentiment, experiments).

## Features

- RAG chat answering **only from the knowledge base** (guardrails + traceability)
- Session-based memory stored in PostgreSQL
- Intent classification (Transactional / Informational / General)
- Human handoff trigger (frustration / repeated failures / negative sentiment)
- Ingestion pipeline (CSV FAQs + PDFs) → chunk → embed → Pinecone upsert
- Analytics endpoint (`GET /analytics`) + offline RAG evaluation
- Next.js web UI (chat, history, analytics)

## Documentation

Full documentation lives in **[`Docs/`](Docs/README.md)**:

| Guide | Description |
|-------|-------------|
| [Setup](Docs/SETUP.md) | Local dev, Docker, DB init, ingestion |
| [Architecture](Docs/ARCHITECTURE.md) | System design and data flow |
| [API Reference](Docs/API.md) | REST endpoints and examples |
| [Configuration](Docs/CONFIGURATION.md) | Environment variables |
| [Development](Docs/DEVELOPMENT.md) | Structure, tests, experiments |
| [Frontend](Docs/FRONTEND.md) | Next.js UI |
| [Demo (Docker)](Docs/DEMO_README.md) | Curl walkthrough |
| [Deploy (Render)](Docs/DEPLOY_RENDER.md) | Production blueprint |

## Quickstart

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Fill `.env` with OpenAI and Pinecone keys, then:

```bash
docker compose up -d postgres
python -m src.models.init_db
python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv
uvicorn src.main:app --reload
```

- API docs: http://localhost:8000/docs
- Frontend: `cd frontend && npm install && npm run dev` → http://localhost:3000

See [Setup Guide](Docs/SETUP.md) for the full walkthrough.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/session` | Create a chat session |
| `POST` | `/chat` | Chat with RAG + memory |
| `GET` | `/history?session_id=...` | Session history |
| `GET` | `/analytics` | Aggregate metrics |
| `GET` | `/health` | Dependency health checks |

## Tech stack

Python 3.11 · FastAPI · OpenAI · Pinecone · PostgreSQL · Next.js 16 · Docker · Render

## Project spec

See [`RESOURCES/PROJECT_SPEC.md`](RESOURCES/PROJECT_SPEC.md) for original requirements.

## Notes

Use a **virtual environment** or **Docker** to avoid dependency conflicts. For reliable installs on Windows, prefer `python -m venv .venv` before `pip install`.
