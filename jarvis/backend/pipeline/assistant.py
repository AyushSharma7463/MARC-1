from backend.core.logger import get_logger
from backend.llm.factory import create_llm
from backend.pipeline.intent_router import IntentRouter
from backend.tools.calculator import calculate


class Assistant:
    """
    Main Assistant Pipeline

    Responsibilities:
    - Receive user input
    - Detect intent
    - Call tools if needed
    - Build prompts
    - Talk to the LLM
    - Maintain conversation memory
    - Summarize long conversations
    """

    def __init__(self):
        self.llm = create_llm()
        self.router = IntentRouter()
        self.logger = get_logger("Assistant")

        self.history = []
        self.summary = ""

    def summarize_history(self) -> str:
        """
        Summarize older conversation history once it becomes large.
        """

        if len(self.history) < 12:
            return self.summary

        summary_input = "\n".join(
            f"{role}: {message}"
            for role, message in self.history[:-6]
        )

        prompt = f"""
Summarize the following conversation.

Keep only:
- Important facts
- User preferences
- Important context

Ignore greetings and small talk.

Conversation:

{summary_input}

Summary:
"""

        try:
            summary = self.llm.generate(prompt).strip()

            if summary:
                return summary

            return self.summary

        except Exception:
            return self.summary

    def build_prompt(self, user_input: str) -> str:
        """
        Build the prompt sent to the LLM.
        """

        new_summary = self.summarize_history()

        if new_summary:
            self.summary = new_summary

        recent_context = "\n".join(
            f"{role}: {message}"
            for role, message in self.history[-6:]
        )

        system_prompt = """
You are Jarvis.

Identity Rules:
- Your name is Jarvis.
- Never invent another identity.
- Never claim to be another person.
- Never say your name is Holden, ChatGPT, Claude, Gemini, or any other assistant.
- Stay in character.

Communication Style:
- Professional
- Friendly
- Concise
- Helpful

If the user calls you Jarvis,
respond naturally as Jarvis.
"""

        return f"""
{system_prompt}

Conversation Summary:
{self.summary}

Recent Conversation:
{recent_context}

User: {user_input}
Jarvis:
"""

    def chat(self, user_input: str) -> str:
        """
        Main conversation pipeline.
        """

        intent = self.router.classify(user_input)

        self.logger.info(f"Intent: {intent}")
        self.logger.info(f"User input: {user_input}")

        if intent == "tool":
            response = calculate(user_input)

        else:
            prompt = self.build_prompt(user_input)

            try:
                response = self.llm.generate(prompt)

            except Exception as e:
                self.logger.error(f"LLM Error: {e}")
                response = "Sorry, I couldn't process that request."

        self.history.append(("User", user_input))
        self.history.append(("Jarvis", response))

        return response