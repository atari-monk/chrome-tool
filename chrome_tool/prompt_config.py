from dataclasses import dataclass


@dataclass
class PromptConfig:
    printPrompt:bool=False
    input_area_id: str = "prompt-textarea"