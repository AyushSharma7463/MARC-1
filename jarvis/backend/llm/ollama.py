import time
import requests

from backend.core.logger import get_logger
from backend.llm.models import LLMConfig


class OllamaClient:
    """
    Client for communicating with the local Ollama server.
    """

    def __init__(self, config: LLMConfig | None = None):
        self.config = config or LLMConfig()
        self.logger = get_logger("LLM")

    def generate(self, prompt: str) -> str:
        start = time.time()

        self.logger.info("Request sent to Ollama")

        url = f"{self.config.host}/api/generate"

        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
            },
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            result = response.json().get("response", "")

            duration = round(time.time() - start, 2)

            self.logger.info(
                f"Response received in {duration}s"
            )

            return result

        except requests.exceptions.ConnectionError:
            self.logger.error("Could not connect to Ollama server at " + self.config.host)
            return "I could not connect to my language model backend. Please make sure Ollama is running."

        except Exception as e:
            self.logger.error(
                f"Ollama request failed: {e}"
            )
            return f"I encountered an error generating a response: {e}"
