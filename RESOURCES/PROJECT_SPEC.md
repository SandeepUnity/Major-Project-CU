Project Specification: AI-Powered Chatbot for EmpowerTech Solutions
Target Program: MSc in Data Science

Architecture Style: Retrieval-Augmented Generation (RAG)

1. System Overview
The goal is to build a production-grade RAG chatbot for EmpowerTech Solutions, an online education platform based in Chennai. The system will provide 24/7 personalized support for enrollment, course queries, and technical issues, reducing instructor bandwidth and improving user satisfaction.

2. Technical Stack (Context for Copilot)
Language: Python 3.10+

API Framework: FastAPI (for high-performance REST endpoints)

LLM Orchestration: LangChain or LlamaIndex

Vector Database: Pinecone (Serverless)

Embeddings: text-embedding-3-small (OpenAI)

Primary LLM: gpt-4o or llama-3-70b

Database: PostgreSQL (for chat history and user metadata)

3. Functional Requirements
Core Chat Capabilities
Semantic Retrieval: Must answer questions based only on the provided EmpowerTech knowledge base (FAQs, course PDFs, policies).

Intent Classification: Distinguish between "Transactional" (enrollment/payment) and "Informational" (how-to/course details) queries.

Contextual Memory: Support multi-turn conversations by maintaining a session-based chat history.

Human Handoff Trigger: Detect user frustration or complex technical failures and suggest escalation to a support agent.

Data Science & Analytics (MSc Requirements)
Sentiment Analysis: Perform real-time sentiment scoring on user queries to measure satisfaction.

Response Evaluation: Implement RAGAS or TruLens metrics (Faithfulness, Relevancy, Answer Correctness) for Chapter 7 analysis.

4. System Architecture (Implementation Flow)
Ingestion Pipeline: Script to chunk PDFs/CSVs, generate embeddings, and upsert to Pinecone.

Retrieval Engine: Hybrid search (Semantic + Keyword) to find relevant context.

Augmentation Layer: Construct a prompt containing System Message + Context + Chat History + User Query.

API Layer: Secure FastAPI routes for /chat, /history, and /analytics.

5. Security & Constraints
Data Privacy: Collect only necessary user IDs; encrypt PII data in transit.

Hallucination Guardrails: If the answer is not in the context, the bot must reply: "I'm sorry, I don't have that information. Would you like to speak with an advisor?".