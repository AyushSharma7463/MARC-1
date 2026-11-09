from backend.skills.calculator import CalculatorSkill
from backend.skills.llm import LLMSkill
from backend.skills.browser import BrowserSkill
from backend.skills.filesystem import FilesystemSkill
from backend.skills.terminal import TerminalSkill
from backend.skills.vision import VisionSkill


class SkillRegistry:
    """
    Stores all available skills.

    The Executor asks the registry for a skill by name.
    """

    def __init__(self):
        self.skills = {}

        self.register(CalculatorSkill())
        self.register(LLMSkill())
        self.register(BrowserSkill())
        self.register(FilesystemSkill())
        self.register(TerminalSkill())
        self.register(VisionSkill())

    # ----------------------------------

    def register(self, skill):
        """
        Register a new skill.
        """
        self.skills[skill.name] = skill

    # ----------------------------------

    def get(self, name):
        """
        Return a skill by name.
        """
        return self.skills.get(name)

    # ----------------------------------

    def has(self, name):
        """
        Check whether a skill exists.
        """
        return name in self.skills

    # ----------------------------------

    def list(self):
        """
        Return all registered skill names.
        """
        return sorted(self.skills.keys())
