import subprocess
from backend.skills.base import Skill
from backend.core.logger import get_logger


class TerminalSkill(Skill):

    name = "terminal"

    description = "Executes safe terminal commands."

    FORBIDDEN_COMMANDS = {
        "rm", "rmdir", "mkfs", "dd", "format", "shutdown", "reboot",
        ":(){ :|:& };:", "kill", "killall", "pkill"
    }

    def __init__(self):
        self.logger = get_logger("TerminalSkill")

    def execute(self, **kwargs) -> str:
        cmd = kwargs.get("command", "").strip()
        if not cmd:
            return "No command provided to execute."

        parts = cmd.split()
        first_token = parts[0].lower() if parts else ""

        if first_token in self.FORBIDDEN_COMMANDS or any(f in cmd for f in ["rm -rf", "> /dev"]):
            self.logger.warning(f"Blocked dangerous command: {cmd}")
            return f"Command '{cmd}' is blocked for safety reasons."

        try:
            res = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = (res.stdout or res.stderr).strip()
            if not output:
                return f"Command '{cmd}' completed with code {res.returncode}."
            # Limit length for speech synthesis
            lines = output.splitlines()[:5]
            return "\n".join(lines)

        except subprocess.TimeoutExpired:
            return f"Command '{cmd}' timed out after 10 seconds."
        except Exception as e:
            self.logger.error(f"Command execution error: {e}")
            return f"Command execution failed: {e}"
