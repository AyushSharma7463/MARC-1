import re
from backend.brain.plan import Plan
from backend.tools.calculator import extract_math_expression, calculate


class Planner:
    """
    Converts user requests into executable plans.

    The Planner decides *what* should be done.
    It does NOT execute anything.
    """

    def create_plan(self, text: str) -> Plan:
        """
        Analyze user input and return a structured Plan.
        """
        text = text.strip()
        lower = text.lower()

        # -----------------------------
        # 1. Calculator
        # -----------------------------
        math_expr = extract_math_expression(text)
        if math_expr is not None:
            # Verify if it computes
            calc_test = calculate(text)
            if calc_test != "Invalid expression":
                return Plan(
                    skill="calculator",
                    goal="Solve a mathematical expression",
                    arguments={"expression": text},
                    confidence=1.0,
                    reasoning="Detected valid mathematical expression."
                )

        # -----------------------------
        # 2. Terminal
        # -----------------------------
        terminal_patterns = [
            r"\b(run\s+command|terminal\s+command|execute\s+command|shell\s+command)\b",
            r"^(run|execute)\s+(ls|pwd|whoami|date|uname|uptime|python)",
        ]
        if any(re.search(pat, lower) for pat in terminal_patterns):
            # Extract actual command if possible
            cmd = re.sub(r"^(run|execute)\s+(command\s+)?", "", text, flags=re.IGNORECASE).strip()
            return Plan(
                skill="terminal",
                goal="Execute terminal command",
                arguments={"command": cmd or text},
                confidence=0.85,
                reasoning="Detected explicit terminal command request."
            )

        # -----------------------------
        # 3. Filesystem
        # -----------------------------
        filesystem_patterns = [
            r"\b(list\s+files|show\s+files|directory\s+contents|folder\s+contents)\b",
            r"\b(current\s+directory|working\s+directory|what\s+folder\s+am\s+i\s+in)\b",
            r"\b(check\s+if\s+file\s+exists)\b",
        ]
        if any(re.search(pat, lower) for pat in filesystem_patterns):
            return Plan(
                skill="filesystem",
                goal="Perform filesystem operation",
                arguments={"request": text},
                confidence=0.85,
                reasoning="Detected filesystem request."
            )

        # -----------------------------
        # 4. Browser / Search
        # -----------------------------
        browser_patterns = [
            r"^(search\s+for|search\s+the\s+web\s+for|google|look\s+up)\b",
            r"\bweather\s+in\b",
        ]
        if any(re.search(pat, lower) for pat in browser_patterns):
            query = re.sub(r"^(search\s+for|search\s+the\s+web\s+for|google|look\s+up)\s+", "", text, flags=re.IGNORECASE).strip()
            return Plan(
                skill="browser",
                goal="Search the internet",
                arguments={"query": query or text},
                confidence=0.90,
                reasoning="Detected web search request."
            )

        # -----------------------------
        # 5. Default → LLM
        # -----------------------------
        return Plan(
            skill="llm",
            goal="Generate conversational response",
            arguments={"prompt": text},
            confidence=0.95,
            reasoning="Conversational input routed to LLM."
        )
