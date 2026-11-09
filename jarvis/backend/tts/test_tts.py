import sys
from pathlib import Path

# Ensure jarvis root is in sys.path
CURRENT = Path(__file__).resolve()
# parents[0] = tts, parents[1] = backend, parents[2] = jarvis, parents[3] = MARC-1
JARVIS_ROOT = CURRENT.parents[2]
if str(JARVIS_ROOT) not in sys.path:
    sys.path.insert(0, str(JARVIS_ROOT))
PROJECT_ROOT = CURRENT.parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.tts.piper import PiperTTS


def main():
    tts = PiperTTS()
    tts.speak("Hello MARC is now working correctly")


def test_piper_initialization():
    tts = PiperTTS()
    assert tts.model_path.exists()


if __name__ == "__main__":
    main()
