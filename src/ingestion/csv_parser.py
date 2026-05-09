from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import Optional


@dataclass
class FAQItem:
    source_id: str
    question: str
    answer: str
    category: Optional[str] = None
    tags: Optional[str] = None

    def as_text(self) -> str:
        parts = [f"Q: {self.question}", f"A: {self.answer}"]
        if self.category:
            parts.append(f"Category: {self.category}")
        if self.tags:
            parts.append(f"Tags: {self.tags}")
        return "\n".join(parts)


def load_faq_csv(path: str) -> list[FAQItem]:
    items: list[FAQItem] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_id = str(row.get("id") or row.get("question_id") or "")
            q = str(row.get("question") or "").strip()
            a = str(row.get("answer") or "").strip()
            if not q or not a:
                continue
            items.append(
                FAQItem(
                    source_id=source_id or q[:32],
                    question=q,
                    answer=a,
                    category=(row.get("category") or None),
                    tags=(row.get("tags") or None),
                )
            )
    return items

