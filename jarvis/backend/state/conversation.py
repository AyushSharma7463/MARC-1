import time

try:
    from backend.core.logger import get_logger
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    sys.path.append(str(project_root))

    from backend.core.logger import get_logger


class ConversationManager:
    """
    Manages:
    - Active / Sleep state
    - Timeout handling
    - Voice commands (sleep/exit)
    """

    def __init__(self, timeout: int = 60):
        self.logger = get_logger("ConversationManager")

        self._active = False
        self.timeout = timeout
        self.last_interaction = None

    # -------------------------
    # State control
    # -------------------------

    def activate(self):
        self._active = True
        self.refresh()
        self.logger.info("Conversation activated.")

    def deactivate(self):
        if self._active:
            self.logger.info("Conversation ended.")

        self._active = False
        self.last_interaction = None

    def is_active(self) -> bool:
        return self._active

    # -------------------------
    # Timeout logic
    # -------------------------

    def refresh(self):
        self.last_interaction = time.time()

    def has_timed_out(self) -> bool:
        if not self._active or self.last_interaction is None:
            return False

        return (time.time() - self.last_interaction) > self.timeout

    # -------------------------
    # NEW: Voice command handler
    # -------------------------

    EXIT_COMMANDS = {
        "exit",
        "quit",
        "shutdown",
        "goodbye",
        "stop",
        "stop listening",
    }

    SLEEP_COMMANDS = {
        "sleep",
        "go to sleep",
        "go sleep",
        "rest",
    }

    def handle_commands(self, text: str):
        """
        Returns:
        - "exit" → shutdown program
        - "sleep" → go inactive
        - None → normal flow
        """

        if not text:
            return None

        t = text.lower().strip()

        if t in self.EXIT_COMMANDS:
            self.logger.info("Exit command detected.")
            return "exit"

        if t in self.SLEEP_COMMANDS:
            self.logger.info("Sleep command detected.")
            return "sleep"

        return None