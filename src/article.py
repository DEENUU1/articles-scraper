from dataclasses import dataclass
from typing import Optional


@dataclass
class Article:
    url: str
    title: str
    description: Optional[str] = None
    ai_summary: Optional[str] = None
