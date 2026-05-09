# Demo Run Instructions (Local)

This project can be demoed locally using Docker Compose (PostgreSQL + API).

## Prerequisites

- Docker Desktop
- An `.env` file (copy from `.env.example`)

## 1) Create `.env`

Create `.env` in the repo root:

- `DATABASE_URL` should point to the compose Postgres service:
  - `postgresql://postgres:postgres@postgres:5432/empowertech_chatbot`
- Fill `OPENAI_API_KEY` and `PINECONE_API_KEY` if you want full RAG + ingestion.

## 2) Start services

```bash
docker compose up --build
```

API will be available at `http://localhost:8000`.

Swagger: `http://localhost:8000/docs`

## 3) Initialize DB tables

In a second terminal (host machine):

```bash
python -m src.models.init_db
python -m src.models.seed_db
```

## 4) (Optional) Ingest sample FAQs into Pinecone

Make sure the Pinecone index named in `PINECONE_INDEX_NAME` already exists, then:

```bash
python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv
```

## 5) Try the API

### Create a session

```bash
curl -X POST "http://localhost:8000/session" -H "Content-Type: application/json" -d "{\"user_id\":\"user_1\"}"
```

### Chat

```bash
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"user_id\":\"user_1\",\"session_id\":\"<SESSION_ID>\",\"query\":\"How do I enroll in a course?\"}"
```

### History

```bash
curl "http://localhost:8000/history?session_id=<SESSION_ID>"
```

### Analytics

```bash
curl "http://localhost:8000/analytics"
```

