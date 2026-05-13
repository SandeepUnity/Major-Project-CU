"""Detect short conversational messages that should not require RAG context."""

from __future__ import annotations

import re

# Whole-message patterns only; keep length check so substantive questions are not misclassified.
_MAX_LEN = 140

_COMBINED = re.compile(
    r"""
    ^(?:
        h+i+!* |
        h+i+\s+t+h+e+r+e+!* |
        h+e+l+o+!* |
        h+e+l+o+\s+t+h+e+r+e+!* |
        h+e+y+!* |
        h+e+y+\s+t+h+e+r+e+!* |
        h+i+y+a+!* |
        h+o+w+d+y+!* |
        g+r+e+e+t+i+n+g+s+!* |
        g+m+!* |
        g+n+!* |
        g+o+o+d+\s+(m+o+r+n+i+n+g|a+f+t+e+r+n+o+o+n|e+v+e+n+i+n+g|d+a+y)\b[!.,\s]* |
        h+o+w+\s+a+r+e+\s+y+o+u+\??[!.,\s]* |
        h+o+w+\s+a+r+e+\s+y+a+\s+d+o+i+n+g+\??[!.,\s]* |
        h+o+w+['']?s+\s+i+t+\s+g+o+i+n+g+\??[!.,\s]* |
        w+h+a+t+['']?s+\s+u+p+\??[!.,\s]* |
        h+o+w+\s+d+o+\s+y+o+u+\s+d+o+\??[!.,\s]* |
        y+o+u+\s+a+l+r+i+g+h+t+\??[!.,\s]* |
        a+r+e+\s+y+o+u+\s+o+k+a+y+\??[!.,\s]* |
        e+v+e+r+y+t+h+i+n+g+\s+o+k+\??[!.,\s]* |
        w+h+o+\s+a+r+e+\s+y+o+u+\??[!.,\s]* |
        w+h+a+t+\s+a+r+e+\s+y+o+u+\??[!.,\s]* |
        w+h+a+t+\s+i+s+\s+y+o+u+r+\s+n+a+m+e+\??[!.,\s]* |
        w+h+a+t+\s+c+a+n+\s+y+o+u+\s+d+o+\??[!.,\s]* |
        w+h+a+t+\s+d+o+\s+y+o+u+\s+d+o+\??[!.,\s]* |
        i+n+t+r+o+d+u+c+e+\s+y+o+u+r+s+e+l+f+[!.,\s]* |
        t+e+l+l+\s+m+e+\s+a+b+o+u+t+\s+y+o+u+r+s+e+l+f+[!.,\s]* |
        n+i+c+e+\s+t+o+\s+m+e+e+t+\s+y+o+u+[!.,\s]* |
        t+h+a+n+k+s+!* |
        t+h+a+n+k+\s+y+o+u+[!.,\s]* |
        t+h+x+!* |
        t+y+!* |
        b+y+e+!* |
        g+o+o+d+b+y+e+[!.,\s]* |
        s+e+e+\s+y+o+u+[!.,\s]* |
        c+h+e+e+r+s+!* |
        c+i+a+o+!* |
        o+k+a+y+!* |
        o+k+!* |
        s+u+p+!*
    )$
    """,
    re.I | re.VERBOSE,
)


def is_small_talk_message(text: str) -> bool:
    q = text.strip()
    if not q or len(q) > _MAX_LEN:
        return False
    return bool(_COMBINED.match(q))
