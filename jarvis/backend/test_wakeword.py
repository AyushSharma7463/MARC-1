from backend.wakeword.detector import WakeWordDetector


def test_wakeword():
    detector = WakeWordDetector()

    assert detector.detect("hey jarvis what time is it")[0] is True
    assert detector.detect("hey marc")[0] is True
    assert detector.detect("hello jarvis")[0] is True
    assert detector.detect("what is the weather")[0] is False
    assert detector.detect("")[0] is False


if __name__ == "__main__":
    detector = WakeWordDetector()
    tests = [
        "Hello MARC",
        "Hey MARC",
        "Hi MARC",
        "Ok MARC",
        "Okay MARC",
        "MARC",
        "What is Python?",
        "Tell me a joke",
        "",
    ]
    for text in tests:
        print(f"{text!r:25} -> {detector.detect(text)}")
