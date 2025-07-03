from selenium import webdriver
from dataclasses import dataclass


@dataclass
class PromptConfig:
    driver: webdriver.Chrome
    prompt: str
    printPrompt:bool=False
    input_area_id: str = "prompt-textarea"