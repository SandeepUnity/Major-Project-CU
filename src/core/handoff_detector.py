from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class HandoffDecision:
    should_handoff: bool
    reason: Optional[str] = None
    severity: str = "low"  # low|medium|high


FRUSTRATION_PAT = re.compile(
    r"\b(not working|doesn't work|error|broken|angry|frustrated|confused|worst|hate|useless)\b",
    re.I,
)
HUMAN_PAT = re.compile(r"\b(human|agent|advisor|representative|support staff)\b", re.I)


class HandoffDetector:
    def should_handoff(
        self,
        user_query: str,
        sentiment_score: Optional[float],
        retrieval_confidence: Optional[float],
        repeated_failures: int = 0,
    ) -> HandoffDecision:
        q = user_query.strip()
        if HUMAN_PAT.search(q):
            return HandoffDecision(True, reason="explicit_request", severity="high")
        if FRUSTRATION_PAT.search(q):
            return HandoffDecision(True, reason="frustration_keywords", severity="medium")
        if sentiment_score is not None and sentiment_score < -0.5:
            return HandoffDecision(True, reason="negative_sentiment", severity="medium")
        if retrieval_confidence is not None and retrieval_confidence < 0.2:
            return HandoffDecision(True, reason="retrieval_failure", severity="medium")
        if repeated_failures >= 3:
            return HandoffDecision(True, reason="repeated_failures", severity="high")
        return HandoffDecision(False)

