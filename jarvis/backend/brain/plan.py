from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Plan:
    """
    A structured execution plan created by the Planner.

    Every user request is converted into a Plan before execution.
    """

    skill: str
    goal: str

    arguments: dict[str, Any] = field(default_factory=dict)

    confidence: float = 1.0

    reasoning: str = ""

    def __repr__(self) -> str:
        return (
            f"Plan("
            f"skill={self.skill}, "
            f"goal={self.goal}, "
            f"confidence={self.confidence:.2f}"
            f")"
        )