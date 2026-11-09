from backend.llm.ollama import OllamaClient
class IntentRouter:
    def __init__(self):
        self.llm = OllamaClient()

    def classify(self, user_input: str) -> str:
        prompt = f"""
Classify the user input into ONE category only.

Categories:
- tool (math, calculation, system operations)
- chat (normal conversation)

Return ONLY one word: tool or chat.

Input: {user_input}
"""

        result = self.llm.generate(prompt).strip().lower()

        if "tool" in result:
            return "tool"

        return "chat"