from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRule:
    content: str
    order: int
    name: str