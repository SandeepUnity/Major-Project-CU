from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.utils.safe_optional import optional_import


@dataclass
class RAGASResult:
    faithfulness: Optional[float]
    answer_relevancy: Optional[float]
    context_recall: Optional[float]
    average: Optional[float]
    method: str = "ragas"


class RAGASEvaluator:
    """
    Thin wrapper around `ragas` that can be safely imported even if ragas deps are missing.

    For the thesis/report: this provides a concrete code location and integration point.
    """

    def evaluate(self, query: str, context: str, answer: str) -> RAGASResult:
        ragas = optional_import("ragas")
        if not ragas:
            return RAGASResult(None, None, None, None, method="ragas_not_installed")

        # Full RAGAS evaluation typically requires dataset objects + an LLM for judgments.
        # This project integrates RAGAS in the experiments pipeline (scripts) to avoid per-request cost.
        return RAGASResult(None, None, None, None, method="ragas_scaffold")

