from backend.brain.planner import Planner
from backend.brain.executor import Executor
from backend.skills.registry import SkillRegistry
from backend.tools.calculator import calculate, extract_math_expression


def test_calculator_tool():
    assert calculate("2 + 2") == "4"
    assert calculate("100 / 4") == "25"
    assert calculate("5 * 20") == "100"
    assert calculate("what is 15 plus 25?") == "40"
    assert calculate("calculate 10 - 3") == "7"


def test_extract_math():
    assert extract_math_expression("what is 10 + 20") is not None
    assert extract_math_expression("hello world") is None
    assert extract_math_expression("what is C++?") is None


def test_planner_routing():
    planner = Planner()

    # Math
    p1 = planner.create_plan("what is 15 * 3?")
    assert p1.skill == "calculator"

    # Conversational (should not route to math even if it contains + or -)
    p2 = planner.create_plan("What is C++?")
    assert p2.skill == "llm"

    p3 = planner.create_plan("How are you doing today?")
    assert p3.skill == "llm"

    # Terminal
    p4 = planner.create_plan("run command date")
    assert p4.skill == "terminal"

    # Filesystem
    p5 = planner.create_plan("list files in current directory")
    assert p5.skill == "filesystem"


def test_skills_registry():
    registry = SkillRegistry()
    assert registry.has("calculator")
    assert registry.has("llm")
    assert registry.has("browser")
    assert registry.has("filesystem")
    assert registry.has("terminal")
    assert registry.has("vision")


def test_executor_with_skills():
    executor = Executor()
    planner = Planner()

    # Test calculator execution
    plan = planner.create_plan("what is 50 * 2?")
    result = executor.execute(plan)
    assert "100" in result

    # Test filesystem execution
    plan = planner.create_plan("show current directory")
    result = executor.execute(plan)
    assert "working directory" in result.lower() or "current" in result.lower()

    # Test terminal safe command
    plan = planner.create_plan("run command echo hello")
    result = executor.execute(plan)
    assert "hello" in result
