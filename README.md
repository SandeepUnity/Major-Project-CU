# EmpowerTech RAG Chatbot (MSc Data Science Major Project)

Production-grade **Retrieval-Augmented Generation (RAG)** chatbot for EmpowerTech Solutions (online education platform). The system provides 24/7 support and produces **thesis-ready analytics** (RAG quality metrics, sentiment, experiments).

## Features

- RAG chat answering **only from knowledge base** (guardrails + traceability)
- Session-based memory stored in PostgreSQL
- Intent classification (Transactional / Informational / General)
- Human handoff trigger (frustration / repeated failures / negative sentiment)
- Ingestion pipeline (CSV FAQs + PDFs) → chunk → embed → Pinecone upsert
- Basic analytics endpoint (`GET /analytics`) + evaluation scaffolding

## Quickstart (Local)

### 1) Setup environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Fill `.env` with your OpenAI + Pinecone keys.

### 2) Start PostgreSQL

Use Docker (recommended):

```bash
docker compose up -d postgres
```

### 3) Initialize database

```bash
python -m src.models.init_db
python -m src.models.seed_db
```

### 4) Ingest sample data (optional)

```bash
python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv
```

### 5) Run API

```bash
uvicorn src.main:app --reload
```

Open Swagger UI at `http://localhost:8000/docs`.

## Endpoints

- `POST /session` create a session
- `POST /chat` chat with RAG + memory
- `GET /history?session_id=...` session history
- `GET /analytics` minimal spec-required analytics summary
- `GET /health` dependency health checks

## Demo (Docker Compose)

See `docs/DEMO_README.md`.

## Important (recommended)

For reliable installs and to avoid conflicts with other Python packages on your system, use a **virtual environment** (`python -m venv .venv`) or run via **Docker**.

## Notes for Report (Chapter 5–7 evidence)

- Screenshots: Swagger UI, sample `/chat` runs, ingestion logs, analytics JSON outputs
- Stored traceability: retrieved chunks/sources are stored with each assistant response
