# API Reference

Base URL (local): `http://localhost:8000`

Interactive docs: **`/docs`** (Swagger UI) and **`/redoc`**

## Endpoints summary

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service and dependency status |
| `POST` | `/session` | Create a new chat session |
| `POST` | `/chat` | Send a message; returns RAG response |
| `GET` | `/history` | List messages for a session |
| `GET` | `/analytics` | Aggregate session/message metrics |

---

## `GET /health`

Health check for PostgreSQL, OpenAI, and Pinecone configuration.

**Response `200`**

```json
{
  "status": "healthy",
  "dependencies": {
    "postgres": "ok",
    "openai": "configured",
    "pinecone": "configured"
  }
}
```

`status` is `degraded` if PostgreSQL is unreachable. OpenAI/Pinecone report `configured` or `not_configured` without making live API calls.

---

## `POST /session`

Create a new chat session for a user.

**Request body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | yes | Client-side user identifier |
| `email` | string | no | Optional email |

```json
{
  "user_id": "user_1",
  "email": "student@example.com"
}
```

**Response `200`**

```json
{
  "session_id": "sess_abc123..."
}
```

---

## `POST /chat`

Send a user query. Creates a session automatically if `session_id` is omitted.

**Request body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | yes | User identifier |
| `session_id` | string | no | Existing session; created if missing |
| `query` | string | yes | User message (1–4000 chars) |

```json
{
  "user_id": "user_1",
  "session_id": "sess_abc123",
  "query": "How do I enroll in a course?"
}
```

**Response `200`**

```json
{
  "response": "To enroll, visit the courses page and click Enroll Now...",
  "session_id": "sess_abc123",
  "confidence": 0.82,
  "handoff_trigger": false,
  "intent": "Transactional",
  "metadata": {
    "model": "gpt-4o",
    "usage": { "prompt_tokens": 450, "completion_tokens": 120, "total_tokens": 570 },
    "retrieval": {
      "confidence": 0.82,
      "top_k": 5,
      "source_ids": ["faq:enrollment-001"]
    },
    "intent": { "intent": "Transactional", "confidence": 0.75 }
  }
}
```

**Error responses**

| Status | When |
|--------|------|
| `400` | Runtime error (e.g. invalid state) |
| `500` | Unexpected server error |

**Metadata routes**

- `metadata.route`: `"small_talk"` for conversational messages
- `metadata.guardrail`: `"no_context"` or `"low_confidence"` on fallback
- `metadata.handoff`: present when escalation is triggered

---

## `GET /history`

Retrieve message history for a session.

**Query parameters**

| Param | Type | Required |
|-------|------|----------|
| `session_id` | string | yes |

**Response `200`**

```json
{
  "session_id": "sess_abc123",
  "messages": [
    {
      "role": "user",
      "content": "How do I enroll?",
      "timestamp": "2026-06-24T10:00:00"
    },
    {
      "role": "assistant",
      "content": "To enroll...",
      "timestamp": "2026-06-24T10:00:02"
    }
  ]
}
```

**Response `404`** — Session not found.

---

## `GET /analytics`

Aggregate metrics for dashboards and thesis analysis.

**Response `200`**

```json
{
  "total_sessions": 42,
  "total_messages": 318,
  "avg_session_sentiment": 0.15,
  "handoff_rate": 0.12
}
```

| Field | Description |
|-------|-------------|
| `total_sessions` | Count of chat sessions |
| `total_messages` | Count of all messages |
| `avg_session_sentiment` | Mean of per-session sentiment averages (nullable) |
| `handoff_rate` | Fraction of sessions with `handoff_triggered = true` |

---

## Example curl session

```bash
# Create session
curl -s -X POST "http://localhost:8000/session" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_1"}'

# Chat (replace SESSION_ID)
curl -s -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_1","session_id":"SESSION_ID","query":"What courses do you offer?"}'

# History
curl -s "http://localhost:8000/history?session_id=SESSION_ID"

# Analytics
curl -s "http://localhost:8000/analytics"
```

## CORS

Local origins `http://localhost:3000` and `http://127.0.0.1:3000` are always allowed. Set `CORS_ORIGINS` (comma-separated) for production frontends.
