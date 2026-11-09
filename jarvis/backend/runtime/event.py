from dataclasses import dataclass, field
from time import time
from typing import Any


@dataclass(slots=True)
class Event:
    """
    Standard event passed through the EventBus.

    Every subsystem communicates using Event objects.
    """

    type: str
    data: dict[str, Any] = field(default_factory=dict)
    source: str = "system"
    timestamp: float = field(default_factory=time)

    def __repr__(self) -> str:
        return (
            f"Event("
            f"type='{self.type}', "
            f"source='{self.source}', "
            f"data={self.data}"
            f")"
        )