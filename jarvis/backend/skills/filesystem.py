import os
from pathlib import Path
from backend.skills.base import Skill
from backend.core.logger import get_logger


class FilesystemSkill(Skill):

    name = "filesystem"

    description = "Handles safe local filesystem operations such as listing or checking files."

    def __init__(self):
        self.logger = get_logger("FilesystemSkill")

    def execute(self, **kwargs) -> str:
        request = kwargs.get("request", "").lower().strip()
        path_str = kwargs.get("path", ".")

        try:
            target = Path(path_str).resolve()

            if any(w in request for w in ["current", "where am i", "pwd", "working directory"]):
                return f"The current working directory is {Path.cwd()}."

            if any(w in request for w in ["list", "files", "contents", "directory", "folder", "ls"]):
                items = sorted(os.listdir(target))[:20]
                if not items:
                    return f"Directory {target.name} is empty."
                return f"Contents of {target.name}: {', '.join(items)}"

            if any(w in request for w in ["exist", "check", "find"]):
                exists = target.exists()
                return f"Path {target.name} {'exists' if exists else 'does not exist'}."

            # Default: list current directory
            items = sorted(os.listdir("."))[:15]
            return f"Files in current directory: {', '.join(items)}"

        except Exception as e:
            self.logger.error(f"Filesystem operation error: {e}")
            return f"Filesystem operation failed: {e}"
