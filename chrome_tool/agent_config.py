from dataclasses import dataclass


@dataclass
class AgentConfig:
    page: str
    detach: bool = True