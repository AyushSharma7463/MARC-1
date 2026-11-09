from backend.core.logger import get_logger

from backend.brain.planner import Planner
from backend.brain.executor import Executor


class Orchestrator:
    """
    Coordinates the Brain pipeline.

    User Input
          │
          ▼
      Planner
          │
          ▼
         Plan
          │
          ▼
      Executor
          │
          ▼
       Response
    """

    def __init__(self):
        self.logger = get_logger("Orchestrator")

        self.planner = Planner()
        self.executor = Executor()

    def process(self, text: str) -> str:
        """
        Complete reasoning pipeline.
        """

        self.logger.info(f"Input: {text}")

        plan = self.planner.create_plan(text)

        self.logger.info(
            f"Plan -> "
            f"skill={plan.skill}, "
            f"goal={plan.goal}, "
            f"confidence={plan.confidence:.2f}"
        )

        result = self.executor.execute(plan)

        self.logger.info(f"Result: {result}")

        return result