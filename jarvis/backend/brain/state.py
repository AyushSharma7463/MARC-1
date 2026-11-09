from collections import deque
from backend.core.logger import get_logger


class BrainState:
    """
    Short-term working memory for Brain

    This replaces the messy history list in Assistant.
    """

    def __init__(self, max_size: int = 20):
        self.logger = get_logger("BrainState")

        self.memory = deque(maxlen=max_size)

    def add(self, role: str, content: str):
        self.memory.append({
            "role": role,
            "content": content
        })

    def get_recent(self, limit: int = 10):
        return list(self.memory)[-limit:]

    def clear(self):
        self.memory.clear()

    def format_for_prompt(self):
        """
        Converts memory into LLM-friendly format
        """
        return "\n".join(
            f"{m['role']}: {m['content']}"
            for m in self.memory
        )