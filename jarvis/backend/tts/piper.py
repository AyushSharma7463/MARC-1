import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from threading import Lock

from backend.core.logger import get_logger
from backend.core.settings import settings


class PiperTTS:
    """
    Offline Text-to-Speech using Piper.

    Features
    --------
    - Robust executable finding (PATH, virtualenv bin, or python -m piper)
    - Thread-safe playback
    - Interruptible speech
    - Prevents overlapping audio
    - Automatic temp file cleanup
    """

    def __init__(
        self,
        model_path: str | None = None,
        config_path: str | None = None,
    ):
        self.logger = get_logger("PiperTTS")

        raw_model_path = model_path or settings.PIPER_MODEL
        self.model_path = self._resolve_file(raw_model_path)

        if not self.model_path.exists():
            # Check models directory inside jarvis
            project_model = Path(__file__).resolve().parents[2] / "models" / "en_US-lessac-medium.onnx"
            if project_model.exists():
                self.model_path = project_model
            else:
                raise FileNotFoundError(f"Piper model not found: {raw_model_path}")

        raw_config_path = config_path or settings.PIPER_CONFIG
        self.config_path = self._resolve_file(raw_config_path) if raw_config_path else None
        if self.config_path and not self.config_path.exists():
            # Check next to model
            sibling_config = Path(f"{self.model_path}.json")
            if sibling_config.exists():
                self.config_path = sibling_config
            else:
                self.config_path = None

        self.piper_cmd = self._find_piper_cmd()
        self.player = None
        self.lock = Lock()

        self.logger.info(f"Piper TTS initialized with model {self.model_path.name}")

    @staticmethod
    def _resolve_file(file_path: str) -> Path:
        path = Path(file_path)
        if path.is_absolute() and path.exists():
            return path
        # Try relative to cwd
        if path.exists():
            return path.resolve()
        # Try relative to jarvis directory
        jarvis_dir = Path(__file__).resolve().parents[2]
        candidate = jarvis_dir / file_path
        if candidate.exists():
            return candidate.resolve()
        return path

    def _find_piper_cmd(self) -> list[str]:
        # 1. System PATH
        piper_path = shutil.which("piper")
        if piper_path:
            return [piper_path]

        # 2. Virtual environment bin
        venv_piper = Path(sys.executable).parent / "piper"
        if venv_piper.exists() and os.access(venv_piper, os.X_OK):
            return [str(venv_piper)]

        # 3. Python module
        return [sys.executable, "-m", "piper"]

    def speak(self, text: str):
        """
        Convert text to speech and play it.
        If another speech is already playing, stop it first.
        """
        if not text or not text.strip():
            return

        text = text.strip()

        with self.lock:
            self.stop()
            self.logger.info(f"TTS Input: {text}")

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                output_wav = tmp.name

            try:
                # -------------------------
                # Generate speech
                # -------------------------
                cmd = list(self.piper_cmd) + [
                    "--model",
                    str(self.model_path),
                    "--output_file",
                    output_wav,
                ]

                if self.config_path and self.config_path.exists():
                    cmd.extend(["--config", str(self.config_path)])

                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                _, stderr = process.communicate(input=text)

                if process.returncode != 0:
                    self.logger.error(f"Piper failed (code {process.returncode}):\n{stderr}")
                    return

                # -------------------------
                # Play audio
                # -------------------------
                if sys.platform == "darwin":
                    player_cmd = ["afplay", output_wav]
                elif shutil.which("aplay"):
                    player_cmd = ["aplay", output_wav]
                elif shutil.which("play"):
                    player_cmd = ["play", output_wav]
                else:
                    player_cmd = ["afplay", output_wav]

                self.player = subprocess.Popen(
                    player_cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

                self.logger.info("Playback started")
                self.player.wait()
                self.logger.info("Playback finished")

            except Exception as e:
                self.logger.error(f"Playback error: {e}")

            finally:
                self.player = None
                try:
                    Path(output_wav).unlink(missing_ok=True)
                except Exception:
                    pass

    def stop(self):
        """
        Stop current playback immediately.
        """
        if self.player is not None and self.player.poll() is None:
            self.logger.info("Stopping playback...")
            try:
                self.player.terminate()
                self.player.wait(timeout=0.5)
            except Exception:
                try:
                    self.player.kill()
                except Exception:
                    pass
            finally:
                self.player = None

    def is_playing(self) -> bool:
        """
        Returns True if Piper is currently speaking.
        """
        return self.player is not None and self.player.poll() is None
