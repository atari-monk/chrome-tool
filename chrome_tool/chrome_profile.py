from dataclasses import dataclass
from pathlib import Path


@dataclass
class ChromeProfile:
    path: Path
    name: str