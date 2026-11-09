from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOCAL_MODEL = BASE_DIR / "models" / "en_US-lessac-medium.onnx"
LOCAL_CONFIG = BASE_DIR / "models" / "en_US-lessac-medium.onnx.json"
FALLBACK_MODEL = "/Users/ayushsharma/Downloads/en_US-lessac-medium.onnx"
FALLBACK_CONFIG = "/Users/ayushsharma/Downloads/en_US-lessac-medium.onnx.json"

DEFAULT_MODEL_PATH = str(LOCAL_MODEL if LOCAL_MODEL.exists() else FALLBACK_MODEL)
DEFAULT_CONFIG_PATH = str(LOCAL_CONFIG if LOCAL_CONFIG.exists() else FALLBACK_CONFIG)


class Settings:
    """
    Central application settings.
    """

    # -------------------------
    # LLM
    # -------------------------

    OLLAMA_HOST: str = os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434"
    )

    MODEL: str = os.getenv(
        "MODEL",
        "llama3.2"
    )

    TIMEOUT: int = int(
        os.getenv("TIMEOUT", "120")
    )

    # -------------------------
    # Logging
    # -------------------------

    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    DEBUG: bool = (
        os.getenv("DEBUG", "False").lower() in ("true", "1")
    )

    # -------------------------
    # Piper TTS
    # -------------------------

    PIPER_MODEL: str = os.getenv(
        "PIPER_MODEL",
        DEFAULT_MODEL_PATH
    )

    PIPER_CONFIG: str = os.getenv(
        "PIPER_CONFIG",
        DEFAULT_CONFIG_PATH
    )


settings = Settings()
