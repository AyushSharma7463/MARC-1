try:
    from legacy.microphone_old import Microphone
except ModuleNotFoundError:
    try:
        from jarvis.legacy.microphone_old import Microphone
    except ModuleNotFoundError:
        from microphone_old import Microphone


def test_microphone_init():
    mic = Microphone()
    assert mic.sample_rate == 16000


if __name__ == "__main__":
    mic = Microphone()
    print("Available devices:")
    mic.list_devices()
    print("\nRecording 2 seconds test...")
    audio = mic.record(2)
    print("Audio shape:", audio.shape)
    print("Done!")
