from __future__ import annotations

from types import ModuleType
from typing import Optional


def optional_import(module_name: str) -> Optional[ModuleType]:
    try:
        return __import__(module_name)
    except Exception:
        return None

