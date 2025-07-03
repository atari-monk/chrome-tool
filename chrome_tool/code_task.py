from pathlib import Path
from dataclasses import dataclass


@dataclass
class CodeTask:
    prompt: str
    output_path: Path
    overwrite:bool=False
    json_output: bool = False