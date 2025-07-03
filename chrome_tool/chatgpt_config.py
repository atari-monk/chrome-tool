from dataclasses import dataclass


@dataclass
class ChatGPTConfig:
    page: str
    detach: bool = True