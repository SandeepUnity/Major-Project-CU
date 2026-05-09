from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

from src.config.settings import settings


@dataclass
class LLMResult:
    text: str
    model: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class LLMClient:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self._client = OpenAI(api_key=settings.openai_api_key)

    def chat(self, system: str, user: str) -> LLMResult:
        resp = self._client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
        )
        msg = resp.choices[0].message.content or ""
        usage = resp.usage
        return LLMResult(
            text=msg,
            model=resp.model,
            prompt_tokens=getattr(usage, "prompt_tokens", None),
            completion_tokens=getattr(usage, "completion_tokens", None),
            total_tokens=getattr(usage, "total_tokens", None),
        )

