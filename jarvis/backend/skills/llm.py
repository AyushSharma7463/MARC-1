from backend.skills.base import Skill
from backend.llm.factory import create_llm


class LLMSkill(Skill):

    name = "llm"

    description = "Generates natural language."

    def __init__(self):

        self.model = create_llm()

    def execute(self, **kwargs):

        prompt = kwargs["prompt"]

        return self.model.generate(prompt)