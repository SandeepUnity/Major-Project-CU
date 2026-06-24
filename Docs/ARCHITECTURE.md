# Architecture

## High-level overview

```
┌─────────────────┐     HTTP      ┌──────────────────┐
│  Next.js UI     │ ────────────► │  FastAPI (main)  │
│  (port 3000)    │               │  (port 8000)     │
└─────────────────┘               └────────┬─────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
           ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
           │  PostgreSQL   │      │   Pinecone    │      │    OpenAI     │
           │  sessions,    │      │   vectors     │      │  chat + embed │
           │  messages     │      │               │      │               │
           └───────────────┘      └───────────────┘      └───────────────┘
```

## Request flow (`POST /chat`)

1. **Session resolution** — `ConversationManager` loads or creates a user and chat session.
2. **History load** — Last *N* messages loaded (`CHAT_HISTORY_LIMIT`, default 10).
3. **Intent classification** — Keyword rules first; optional LLM refinement (`IntentClassifier`).
4. **Sentiment analysis** — VADER on user query (`SentimentAnalyzer`).
5. **Route selection**
   - **Small talk** (greetings, thanks) → lightweight LLM reply, no retrieval
   - **Knowledge query** → retrieval + RAG path
6. **Retrieval** — Query embedded via OpenAI; Pinecone returns top-*K* chunks (`Retriever`).
7. **Handoff check** — Frustration keywords, negative sentiment, low retrieval confidence, repeated fallbacks (`HandoffDetector`).
8. **Guardrails** — If no chunks or confidence below threshold, return fallback without LLM:
   > "I'm sorry, I don't have that information. Would you like to speak with an advisor?"
9. **Generation** — `PromptBuilder` assembles system + context + history + query; `LLMClient` calls OpenAI.
10. **Persistence** — User/assistant messages, retrieved context, metadata, and feedback rows stored in PostgreSQL.

## Core modules (`src/core/`)

| Module | Responsibility |
|--------|----------------|
| `chat_orchestrator.py` | End-to-end chat pipeline and routing |
| `conversation_manager.py` | Users, sessions, message CRUD, sentiment averages |
| `retriever.py` | Embed query → Pinecone semantic search |
| `vector_store.py` | OpenAI embedder + Pinecone upsert/query |
| `intent_classifier.py` | Transactional / Informational / General |
| `sentiment_analyzer.py` | VADER (default) or optional LLM sentiment |
| `handoff_detector.py` | Escalation rules |
| `prompt_builder.py` | RAG and small-talk prompt templates |
| `llm_client.py` | OpenAI chat completions wrapper |
| `small_talk.py` | Detect non-KB conversational messages |
| `ragas_evaluator.py` | RAGAS metric scaffolding for evaluation |

## Ingestion pipeline (`src/ingestion/`)

Offline batch process (not triggered by API requests):

```
CSV / PDF  →  parse  →  chunk  →  embed  →  Pinecone upsert
```

| File | Role |
|------|------|
| `ingest.py` | CLI entry point |
| `pipeline.py` | Orchestrates parse → chunk → embed → upsert |
| `csv_parser.py` | FAQ CSV loader |
| `pdf_parser.py` | PDF text extraction (pdfplumber) |
| `chunking.py` | LangChain text splitter wrapper |

Default chunk sizes: CSV 800/120 overlap; PDF 1000/200 overlap.

## Data model (`src/models/database.py`)

```
User 1──* ChatSession 1──* ChatMessage 1──0..1 Feedback
```

- **User** — `user_id` (client-supplied), optional `email`
- **ChatSession** — `session_id`, message count, avg sentiment, handoff flags
- **ChatMessage** — role, content, intent, confidence, `retrieved_context` (JSON), `metadata` (JSON)
- **Feedback** — sentiment, optional RAGAS scores, retrieval settings (for analytics)

Schema is created automatically on API startup (`create_all` in `main.py` lifespan).

## Guardrails and traceability

- Answers are constrained to retrieved context in the system prompt.
- Low-confidence or empty retrieval skips the LLM and returns the spec-mandated fallback.
- Every assistant response stores `retrieved_context` and `metadata` (model, tokens, source IDs) for audit and thesis evidence.

## Handoff triggers

| Condition | Reason code |
|-----------|-------------|
| User asks for human/agent | `explicit_request` |
| Frustration keywords | `frustration_keywords` |
| Sentiment score &lt; −0.5 | `negative_sentiment` |
| Retrieval confidence &lt; 0.2 | `retrieval_failure` |
| ≥ 3 prior fallback responses | `repeated_failures` |
| Guardrail fallback (no/low context) | `no_context` / `low_confidence` |

## Frontend architecture

Single-page chat (`app/page.tsx`) plus `/history` and `/analytics`. The API client (`lib/api.ts`) calls the FastAPI backend. Session ID is persisted in `localStorage`.

See [Frontend](FRONTEND.md) for details.
