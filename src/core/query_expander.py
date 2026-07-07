"""Expand broad topical user queries into retrieval-friendly search text."""

from __future__ import annotations

import re

# (pattern, expanded search query)
_BROAD_TOPIC_RULES: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(
            r"^(?:tell\s+me\s+about|what\s+can\s+you\s+tell\s+me\s+about|"
            r"(?:give\s+me\s+)?(?:some\s+)?info(?:rmation)?\s+about|"
            r"i\s+(?:want|would like)\s+to\s+(?:know|learn)\s+about|"
            r"learn\s+about|overview\s+of|what\s+do\s+you\s+know\s+about)\s+"
            r"(?:the\s+|your\s+)?courses?\??$",
            re.I,
        ),
        "EmpowerTech courses programs offerings prerequisites schedule materials access "
        "self-paced instructor-led bootcamp certification assignments labs",
    ),
    (
        re.compile(
            r"^(?:what\s+courses?\s+(?:do\s+you\s+)?(?:offer|have|provide)|"
            r"(?:list|show)\s+(?:me\s+)?(?:your\s+)?courses?)\??$",
            re.I,
        ),
        "EmpowerTech course catalog offerings programs data science Python bootcamp",
    ),
    (
        re.compile(
            r"^(?:tell\s+me\s+about|what\s+can\s+you\s+tell\s+me\s+about|"
            r"(?:give\s+me\s+)?(?:some\s+)?info(?:rmation)?\s+about|"
            r"i\s+(?:want|would like)\s+to\s+(?:know|learn)\s+about|"
            r"learn\s+about|overview\s+of|how\s+does)\s+"
            r"(?:the\s+|your\s+)?enroll(?:ment|ing)?\s*(?:process)?\??$",
            re.I,
        ),
        "EmpowerTech enroll enrollment process course catalog payment confirmation seat availability",
    ),
    (
        re.compile(
            r"^(?:tell\s+me\s+about|what\s+can\s+you\s+tell\s+me\s+about|"
            r"(?:give\s+me\s+)?(?:some\s+)?info(?:rmation)?\s+about|"
            r"i\s+(?:want|would like)\s+to\s+(?:know|learn)\s+about|"
            r"learn\s+about|overview\s+of)\s+"
            r"(?:the\s+|your\s+)?technical\s+support\??$",
            re.I,
        ),
        "EmpowerTech technical support video browser live class system requirements help contact",
    ),
    (
        re.compile(
            r"^(?:tell\s+me\s+about|what\s+can\s+you\s+tell\s+me\s+about|"
            r"(?:give\s+me\s+)?(?:some\s+)?info(?:rmation)?\s+about|"
            r"i\s+(?:want|would like)\s+to\s+(?:know|learn)\s+about|"
            r"learn\s+about|overview\s+of)\s+"
            r"(?:the\s+|your\s+)?(?:payment|payments|fees?|pricing)\??$",
            re.I,
        ),
        "EmpowerTech payment methods fees EMI invoice receipt refund UPI card GST",
    ),
    (
        re.compile(
            r"^(?:tell\s+me\s+about|what\s+can\s+you\s+tell\s+me\s+about|"
            r"(?:give\s+me\s+)?(?:some\s+)?info(?:rmation)?\s+about|"
            r"i\s+(?:want|would like)\s+to\s+(?:know|learn)\s+about|"
            r"learn\s+about|overview\s+of)\s+"
            r"(?:the\s+|your\s+)?(?:policies?|refund\s+policy)\??$",
            re.I,
        ),
        "EmpowerTech refund policy cancellation terms code of conduct academic integrity",
    ),
]


def expand_query(query: str) -> list[str]:
    """Return one or more search queries (original first, then expansions)."""
    q = query.strip()
    if not q:
        return [q]
    expanded: list[str] = [q]
    for pattern, search_text in _BROAD_TOPIC_RULES:
        if pattern.match(q):
            if search_text not in expanded:
                expanded.append(search_text)
            break
    return expanded


def is_broad_topic_query(query: str) -> bool:
    """True when the user asks for a high-level overview rather than a specific fact."""
    q = query.strip()
    if not q:
        return False
    return len(expand_query(q)) > 1
