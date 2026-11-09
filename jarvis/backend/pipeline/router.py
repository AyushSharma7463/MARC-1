from backend.tools.calculator import calculate


def route(user_input: str):
    # Intent detection for math expressions
    math_keywords = ["+", "-", "*", "/", "calculate", "multiply", "add", "divide"]

    if any(k in user_input for k in math_keywords):
        result = calculate(user_input)
        if result != "Invalid expression":
            return "tool", result

    return "llm", None
