from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from src.core.llm_client import LLMClient
from src.utils.safe_optional import optional_import


@dataclass
class IntentResult:
    intent: str
    confidence: float
    reasoning: Optional[str] = None


TRANSACTIONAL_PAT = re.compile(r"\b(pay|payment|refund|enroll|enrol|register|fee|invoice|receipt)\b", re.I)
INFORMATIONAL_PAT = re.compile(r"\b(course|syllabus|duration|schedule|batch|timing|prerequisite|curriculum)\b", re.I)


class IntentClassifier:
    def __init__(self) -> None:
        self._llm: Optional[LLMClient] = None

    def classify(self, query: str) -> IntentResult:
        q = query.strip()
        if TRANSACTIONAL_PAT.search(q):
            return IntentResult(intent="Transactional", confidence=0.75, reasoning="keyword_match")
        if INFORMATIONAL_PAT.search(q):
            return IntentResult(intent="Informational", confidence=0.7, reasoning="keyword_match")

        # optional LLM refinement when available
        if self._llm is None:
            try:
                self._llm = LLMClient()
            except Exception:
                return IntentResult(intent="General", confidence=0.5, reasoning="fallback_no_llm")

        system = (
            "Classify the user query into exactly one label: Transactional, Informational, General. "
            "Return JSON with keys: intent, confidence (0-1)."
        )
        r = self._llm.chat(system=system, user=q).text
        json_mod = optional_import("json")
        if json_mod:
            try:
                data = json_mod.loads(_extract_json(r))
                return IntentResult(
                    intent=str(data.get("intent", "General")),
                    confidence=float(data.get("confidence", 0.5)),
                    reasoning="llm",
                )
            except Exception:
                pass
        return IntentResult(intent="General", confidence=0.5, reasoning="llm_parse_fallback")


def _extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        return text[start : end + 1]
    return "{}"

