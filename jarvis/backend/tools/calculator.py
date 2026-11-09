import ast
import operator
import re

# Supported safe arithmetic operators
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_ast(node):
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    elif isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type}")
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        return SAFE_OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type}")
        operand = _eval_ast(node.operand)
        return SAFE_OPERATORS[op_type](operand)
    else:
        raise ValueError(f"Unsupported AST node: {type(node)}")


def safe_eval_math(expr: str) -> float | int:
    """
    Safely evaluate an arithmetic expression using the AST module.
    Never uses eval().
    """
    parsed = ast.parse(expr, mode="eval")
    return _eval_ast(parsed)


def extract_math_expression(text: str) -> str | None:
    """
    Extract a valid mathematical expression from natural language text.
    Returns cleaned expression string or None if text is not math.
    """
    if not text:
        return None

    cleaned = text.lower().strip()

    # Convert spoken math words to symbols
    replacements = [
        (r"\bplus\b", "+"),
        (r"\bminus\b", "-"),
        (r"\btimes\b", "*"),
        (r"\bmultiplied\s+by\b", "*"),
        (r"\bdivided\s+by\b", "/"),
        (r"\bover\b", "/"),
        (r"\bto\s+the\s+power\s+of\b", "**"),
        (r"\bmodulo\b", "%"),
        (r"\bmod\b", "%"),
        (r"\^", "**"),
    ]
    for pattern, replacement in replacements:
        cleaned = re.sub(pattern, replacement, cleaned)

    # Remove common prefixes/suffixes
    cleaned = re.sub(
        r"^(what\s+is|calculate|compute|solve|evaluate|find|tell\s+me\s+what\s+is|what's)\s+",
        "",
        cleaned,
    )
    cleaned = cleaned.rstrip("?.!")

    # Must contain at least one digit and at least one arithmetic operator
    if not re.search(r"\d", cleaned):
        return None

    if not re.search(r"[\+\-\*\/\%]", cleaned):
        return None

    # Keep only valid math characters: digits, decimal point, operators, parentheses, spaces
    candidate = "".join(ch for ch in cleaned if ch in "0123456789.+-*/%() \t")
    candidate = candidate.strip()

    # Must still have digits and operators
    if not candidate or not re.search(r"\d", candidate) or not re.search(r"[\+\-\*\/\%]", candidate):
        return None

    return candidate


def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.
    Returns the computed result as a string or 'Invalid expression'.
    """
    try:
        expr = extract_math_expression(expression)
        if not expr:
            # Fallback: check if the string itself is directly evaluable
            expr = expression.strip().rstrip("?.!")

        val = safe_eval_math(expr)

        # Format integer results without trailing .0
        if isinstance(val, float) and val.is_integer():
            val = int(val)
        return str(val)

    except Exception:
        return "Invalid expression"
