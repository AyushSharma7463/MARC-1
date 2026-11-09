import numpy as np
from backend.audio.vad import VoiceActivityDetector


def test_vad():
    vad = VoiceActivityDetector(threshold=0.04)

    # Test silence
    silence = np.zeros(480, dtype=np.float32)
    assert vad.rms(silence) == 0.0
    assert not vad.is_speech(silence)

    # Test loud signal
    loud = np.ones(480, dtype=np.float32)
    assert vad.rms(loud) == 1.0
    assert vad.is_speech(loud)


def run_interactive_mic():
    import sounddevice as sd

    sample_rate = 16000
    chunk_ms = 30
    chunk_size = int(sample_rate * chunk_ms / 1000)
    vad = VoiceActivityDetector(threshold=0.04)

    print("=" * 40)
    print("Voice Activity Detection Interactive Test")
    print("Speak into microphone. Press Ctrl+C to stop.")
    print("=" * 40)

    def callback(indata, frames, time, status):
        audio = np.squeeze(indata)
        energy = vad.rms(audio)
        state = "🟢 SPEECH" if vad.is_speech(audio) else "⚪ SILENCE"
        print(f"Energy: {energy:.5f}  {state}")

    try:
        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            blocksize=chunk_size,
            dtype="float32",
            callback=callback,
        ):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    run_interactive_mic()
