from pathlib import Path
from dataclasses import dataclass


@dataclass
class CodeTask:
    prompt: str
    output_path: Path
    json_output: bool = False
    delay_seconds: int = 25
    overwrite:bool=False