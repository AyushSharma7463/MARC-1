import sys
from pathlib import Path

# Ensure jarvis root is in sys.path
jarvis_dir = Path(__file__).resolve().parent.parent
if str(jarvis_dir) not in sys.path:
    sys.path.insert(0, str(jarvis_dir))

from backend.runtime.bootstrap import build_system


def main():
    engine = build_system()
    engine.start()
    engine.run()


if __name__ == "__main__":
    main()
