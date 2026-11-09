import sys
from pathlib import Path

# Add jarvis root to sys.path
jarvis_dir = Path(__file__).resolve().parent / "jarvis"
if str(jarvis_dir) not in sys.path:
    sys.path.insert(0, str(jarvis_dir))

from backend.runtime.bootstrap import build_system


def main():
    print("=" * 60)
    print("Starting MARC Voice Assistant")
    print("=" * 60)
    engine = build_system()
    engine.start()
    engine.run()


if __name__ == "__main__":
    main()
