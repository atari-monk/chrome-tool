from pathlib import Path
from dataclasses import dataclass
from selenium import webdriver


@dataclass
class CodeBlockConfig:
    driver: webdriver.Chrome
    output_file_path: Path
    json: bool = False
    printResponse:bool=False
    overwrite:bool=False
    use_delay=False
    delay_seconds: int = 0