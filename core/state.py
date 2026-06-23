from dataclasses import dataclass, field


@dataclass
class AgentState:
    goal: str
    iteration: int = 0
    plan: str = ""
    work_output: str = ""
    review: dict = field(default_factory=dict)
    history: list = field(default_factory=list)