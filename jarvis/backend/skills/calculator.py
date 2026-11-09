from backend.skills.base import Skill
from backend.tools.calculator import calculate


class CalculatorSkill(Skill):

    name = "calculator"

    description = "Evaluates mathematical expressions."

    def execute(self, **kwargs):
        expression = kwargs.get("expression", "")
        result = calculate(expression)
        if result == "Invalid expression":
            # If calculator cannot solve, let the caller know
            return f"I could not calculate '{expression}' as a valid mathematical expression."
        return f"The answer is {result}."
