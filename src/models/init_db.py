from __future__ import annotations

from src.models.database import Base
from src.models.db import get_engine


def main() -> None:
    Base.metadata.create_all(bind=get_engine())
    print("DB initialized.")


if __name__ == "__main__":
    main()

