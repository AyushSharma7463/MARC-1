from backend.skills.registry import SkillRegistry
from backend.brain.plan import Plan
from backend.core.logger import get_logger


class Executor:
    """
    Executes Plans produced by the Planner.

    The Executor executes the skill chosen by the Planner.
    If a specialized skill fails, it gracefully falls back to the LLM.
    """

    def __init__(self):
        self.logger = get_logger("Executor")
        self.registry = SkillRegistry()

    def execute(self, plan: Plan) -> str:
        skill = self.registry.get(plan.skill)

        if skill is None:
            self.logger.warning(f"Skill '{plan.skill}' not found, falling back to LLM")
            llm_skill = self.registry.get("llm")
            if llm_skill:
                prompt = (
                    plan.arguments.get("prompt")
                    or plan.arguments.get("query")
                    or plan.arguments.get("request")
                    or plan.arguments.get("command")
                    or plan.arguments.get("expression")
                    or str(plan.arguments)
                )
                return llm_skill.execute(prompt=prompt)
            return f"Skill '{plan.skill}' is not available."

        try:
            result = skill.execute(**plan.arguments)
            return str(result)

        except Exception as e:
            self.logger.error(f"Skill '{plan.skill}' execution failed: {e}")
            # Graceful fallback to LLM
            llm_skill = self.registry.get("llm")
            if llm_skill and plan.skill != "llm":
                try:
                    fallback_prompt = (
                        plan.arguments.get("prompt")
                        or plan.arguments.get("query")
                        or plan.arguments.get("request")
                        or plan.arguments.get("command")
                        or plan.arguments.get("expression")
                    )
                    if fallback_prompt:
                        return llm_skill.execute(prompt=fallback_prompt)
                except Exception:
                    pass
            return f"I encountered an error executing that request: {e}"
