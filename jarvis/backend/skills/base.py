from abc import ABC, abstractmethod
from typing import Any


class Skill(ABC):
    """
    Base class for every MARC skill.

    Every capability (LLM, Calculator, Browser, Vision, etc.)
    inherits from this class.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        Execute the skill.

        Returns the result produced by the skill.
        """
        pass