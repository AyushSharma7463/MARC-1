from backend.skills.base import Skill
from backend.core.logger import get_logger


class VisionSkill(Skill):

    name = "vision"

    description = "Provides visual perception and screen analysis capabilities."

    def __init__(self):
        self.logger = get_logger("VisionSkill")

    def execute(self, **kwargs) -> str:
        query = kwargs.get("query", "Describe what is on screen")
        return f"Vision module ready. Received request: {query}."
