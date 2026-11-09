from backend.core.logger import get_logger
from backend.core.settings import settings


def test_settings():
    assert settings.MODEL is not None
    assert settings.OLLAMA_HOST is not None
    logger = get_logger("MARC")
    logger.info(f"Loaded settings - Model: {settings.MODEL}, Host: {settings.OLLAMA_HOST}")


if __name__ == "__main__":
    test_settings()
    print("Settings test passed.")
