from dataclasses import dataclass


@dataclass
class LLMConfig:
    model: str = "llama3.2"
    host: str = "http://localhost:11434"
    temperature: float = 0.7