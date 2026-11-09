from backend.core.settings import settings
from backend.llm.models import LLMConfig
from backend.llm.ollama import OllamaClient


def create_llm():
    config = LLMConfig(
        model=settings.MODEL,
        host=settings.OLLAMA_HOST,
    )
    return OllamaClient(config)
