from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.core.llm_client import LLMClient
from src.utils.safe_optional import optional_import


@dataclass
class SentimentResult:
    score: float  # [-1, 1]
    label: str  # negative | neutral | positive
    confidence: Optional[float] = None
    method: str = "vader"


class SentimentAnalyzer:
    """
    Default: VADER (offline, lightweight).
    Optional: OpenAI (if OPENAI_API_KEY set) for higher accuracy.
    """

    def __init__(self, prefer_llm: bool = False) -> None:
        self._prefer_llm = prefer_llm
        self._llm: Optional[LLMClient] = None

    def analyze(self, text: str) -> SentimentResult:
        t = text.strip()
        if not t:
            return SentimentResult(score=0.0, label="neutral", confidence=1.0, method="empty")

        if self._prefer_llm:
            if self._llm is None:
                try:
                    self._llm = LLMClient()
                except Exception:
                    self._llm = None
            if self._llm:
                system = (
                    "You are a sentiment analyzer. Score the sentiment of the user text in [-1,1]. "
                    "Return JSON with keys: score, label (negative|neutral|positive), confidence (0-1)."
                )
                out = self._llm.chat(system=system, user=t).text
                json_mod = optional_import("json")
                if json_mod:
                    try:
                        data = json_mod.loads(_extract_json(out))
                        score = float(data.get("score", 0.0))
                        score = max(-1.0, min(1.0, score))
                        label = str(data.get("label", _label(score)))
                        conf = float(data.get("confidence", 0.5))
                        return SentimentResult(score=score, label=label, confidence=conf, method="llm")
                    except Exception:
                        pass

        try:
            # Avoid optional_import for dotted imports; keep this robust in Docker/CI.
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore

            analyzer = SentimentIntensityAnalyzer()
            compound = float(analyzer.polarity_scores(t)["compound"])  # [-1, 1]
            return SentimentResult(score=compound, label=_label(compound), confidence=None, method="vader")
        except Exception:
            pass

        return SentimentResult(score=0.0, label="neutral", confidence=None, method="fallback")


def _label(score: float) -> str:
    if score <= -0.2:
        return "negative"
    if score >= 0.2:
        return "positive"
    return "neutral"


def _extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        return text[start : end + 1]
    return "{}"

