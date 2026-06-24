# EmpowerTech RAG Chatbot — Documentation

Documentation for the MSc Data Science major project: a production-grade **Retrieval-Augmented Generation (RAG)** chatbot for EmpowerTech Solutions (online education platform).

## Quick links

| Document | Description |
|----------|-------------|
| [Setup Guide](SETUP.md) | Local development, Docker Compose, database init, ingestion |
| [Architecture](ARCHITECTURE.md) | System design, data flow, core components |
| [API Reference](API.md) | REST endpoints, request/response schemas, examples |
| [Configuration](CONFIGURATION.md) | Environment variables and tuning parameters |
| [Development](DEVELOPMENT.md) | Project structure, testing, CI, experiments |
| [Frontend](FRONTEND.md) | Next.js UI, pages, API client |
| [Demo (Docker)](DEMO_README.md) | Step-by-step demo with curl examples |
| [Deploy (Render)](DEPLOY_RENDER.md) | Production deployment blueprint |
| [RAG Evaluation](../experiments/README_EVALUATION.md) | Offline retrieval/answer evaluation |

## What this system does

- Answers student support questions **only from the knowledge base** (FAQs, PDFs) with hallucination guardrails
- Maintains **multi-turn session memory** in PostgreSQL
- Classifies intent (Transactional / Informational / General)
- Detects frustration and triggers **human handoff**
- Scores **sentiment** on user messages for analytics
- Exposes **analytics** for thesis/report evidence (sessions, sentiment, handoff rate)
- Provides a **Next.js web UI** for chat, history, and analytics

## Tech stack

| Layer | Technology |
|-------|------------|
| API | Python 3.11+, FastAPI, Uvicorn |
| LLM & embeddings | OpenAI (`gpt-4o`, `text-embedding-3-small`) |
| Vector store | Pinecone (serverless) |
| Relational DB | PostgreSQL 16 |
| Frontend | Next.js 16, React 19, Tailwind CSS 4 |
| Evaluation | Custom metrics + RAGAS (optional) |
| Deployment | Docker, Render Blueprint |

## Minimum quickstart

```bash
python -m venv .venv
.\.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env            # fill OpenAI + Pinecone keys

docker compose up -d postgres
python -m src.models.init_db
python -m src.models.seed_db
python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv

uvicorn src.main:app --reload
```

API docs: `http://localhost:8000/docs`

For the full UI stack, see [Setup Guide](SETUP.md#full-stack-docker-compose).

## Project context

- **Specification:** [`RESOURCES/PROJECT_SPEC.md`](../RESOURCES/PROJECT_SPEC.md)
- **Thesis/report draft:** [`PROJECT_REPORT.md`](PROJECT_REPORT.md)
