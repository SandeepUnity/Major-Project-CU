from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from src.config.settings import settings
from src.core.conversation_manager import ConversationManager
from src.core.handoff_detector import HandoffDetector
from src.core.intent_classifier import IntentClassifier
from src.core.llm_client import LLMClient
from src.core.prompt_builder import PromptBuilder
from src.core.retriever import Retriever
from src.core.sentiment_analyzer import SentimentAnalyzer
from src.models.database import Feedback, MessageRole


FALLBACK_MESSAGE = "I'm sorry, I don't have that information. Would you like to speak with an advisor?"


@dataclass
class ChatResult:
    response: str
    session_id: str
    intent: Optional[str]
    confidence: Optional[float]
    handoff_trigger: bool
    metadata: Dict[str, Any]


class ChatOrchestrator:
    def __init__(self) -> None:
        self._conv = ConversationManager()
        self._retriever = Retriever()
        self._intent = IntentClassifier()
        self._sentiment = SentimentAnalyzer(prefer_llm=False)
        self._handoff = HandoffDetector()
        self._prompts = PromptBuilder()
        self._llm: Optional[LLMClient] = None

    def chat(self, db: Session, user_id: str, session_id: Optional[str], query: str) -> ChatResult:
        user = self._conv.get_or_create_user(db, user_id=user_id)

        session = self._conv.get_session(db, session_id) if session_id else None
        if session is None:
            session = self._conv.create_session(db, user)

        history = self._conv.load_history(db, session, limit=settings.chat_history_limit)
        repeated_failures = sum(
            1 for m in history if m.get("role") == "assistant" and FALLBACK_MESSAGE in (m.get("content") or "")
        )

        intent = self._intent.classify(query)
        sentiment = self._sentiment.analyze(query)

        retrieval = self._retriever.retrieve(query)
        retrieval_conf = retrieval.confidence

        decision = self._handoff.should_handoff(
            user_query=query,
            sentiment_score=sentiment.score,
            retrieval_confidence=retrieval_conf,
            repeated_failures=repeated_failures,
        )

        # Persist user message first (audit trail)
        self._conv.add_message(
            db,
            session,
            role=MessageRole.user,
            content=query,
            intent=intent.intent,
            confidence=intent.confidence,
            metadata={"sentiment": {"score": sentiment.score, "label": sentiment.label, "method": sentiment.method}},
        )

        # Guardrails: if no context or low confidence, return fallback without LLM call.
        no_context = not retrieval.chunks
        low_conf = retrieval_conf is not None and retrieval_conf < settings.retrieval_confidence_threshold
        if no_context or low_conf:
            assistant_text = FALLBACK_MESSAGE
            handoff = True  # treat as handoff hint when KB lacks answer
            reason = "no_context" if no_context else "low_confidence"
            meta = {
                "guardrail": reason,
                "retrieval": {"confidence": retrieval_conf, "top_k": settings.retrieval_top_k, "chunks": []},
                "intent": {"intent": intent.intent, "confidence": intent.confidence},
            }
            assistant_msg = self._conv.add_message(
                db,
                session,
                role=MessageRole.assistant,
                content=assistant_text,
                intent=intent.intent,
                confidence=retrieval_conf,
                retrieved_context=[],
                metadata=meta,
            )
            db.add(
                Feedback(
                    message_id=assistant_msg.id,
                    sentiment_score=sentiment.score,
                    sentiment_label=sentiment.label,
                    retrieval_top_k=settings.retrieval_top_k,
                    notes="guardrail_fallback",
                )
            )
            db.commit()
            return ChatResult(
                response=assistant_text,
                session_id=session.session_id,
                intent=intent.intent,
                confidence=retrieval_conf,
                handoff_trigger=handoff,
                metadata=meta,
            )

        if decision.should_handoff:
            assistant_text = "I understand. Let me connect you with an advisor who can help further."
            meta = {
                "handoff": {"reason": decision.reason, "severity": decision.severity},
                "retrieval": {
                    "confidence": retrieval_conf,
                    "top_k": settings.retrieval_top_k,
                    "source_ids": [_source_id(c) for c in retrieval.chunks],
                },
                "intent": {"intent": intent.intent, "confidence": intent.confidence},
            }
            assistant_msg = self._conv.add_message(
                db,
                session,
                role=MessageRole.assistant,
                content=assistant_text,
                intent=intent.intent,
                confidence=retrieval_conf,
                retrieved_context=[c.metadata for c in retrieval.chunks],
                metadata=meta,
            )
            db.add(
                Feedback(
                    message_id=assistant_msg.id,
                    sentiment_score=sentiment.score,
                    sentiment_label=sentiment.label,
                    retrieval_top_k=settings.retrieval_top_k,
                    notes="handoff_triggered",
                )
            )
            session.handoff_triggered = True
            session.handoff_reason = decision.reason
            db.commit()
            return ChatResult(
                response=assistant_text,
                session_id=session.session_id,
                intent=intent.intent,
                confidence=retrieval_conf,
                handoff_trigger=True,
                metadata=meta,
            )

        if self._llm is None:
            self._llm = LLMClient()
        system, user_prompt = self._prompts.build(query=query, history=history, chunks=retrieval.chunks)
        llm_res = self._llm.chat(system=system, user=user_prompt)

        meta = {
            "model": llm_res.model,
            "usage": {
                "prompt_tokens": llm_res.prompt_tokens,
                "completion_tokens": llm_res.completion_tokens,
                "total_tokens": llm_res.total_tokens,
            },
            "retrieval": {
                "confidence": retrieval_conf,
                "top_k": settings.retrieval_top_k,
                "source_ids": [_source_id(c) for c in retrieval.chunks],
            },
            "intent": {"intent": intent.intent, "confidence": intent.confidence},
        }

        assistant_msg = self._conv.add_message(
            db,
            session,
            role=MessageRole.assistant,
            content=llm_res.text,
            intent=intent.intent,
            confidence=retrieval_conf,
            retrieved_context=[c.metadata for c in retrieval.chunks],
            metadata=meta,
            tokens_used=llm_res.total_tokens,
        )
        db.add(
            Feedback(
                message_id=assistant_msg.id,
                sentiment_score=sentiment.score,
                sentiment_label=sentiment.label,
                retrieval_top_k=settings.retrieval_top_k,
            )
        )
        db.commit()

        return ChatResult(
            response=llm_res.text,
            session_id=session.session_id,
            intent=intent.intent,
            confidence=retrieval_conf,
            handoff_trigger=False,
            metadata=meta,
        )


def _source_id(chunk) -> str:
    return str(chunk.metadata.get("source_id") or chunk.metadata.get("source") or chunk.id)

