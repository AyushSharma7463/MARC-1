from pathlib import Path
from datetime import datetime
import numpy as np
import sounddevice as sd
import soundfile as sf

from backend.audio.vad import VoiceActivityDetector
from backend.core.logger import get_logger
from backend.audio.runtime.microphone_stream import MicrophoneStream


class StreamRecorder:
    """
    Continuously listens to the microphone.

    Starts recording when speech is detected.
    Stops recording after prolonged silence.
    Also provides lightweight speech detection for barge-in support.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_ms: int = 30,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_ms = chunk_ms

        self.chunk_size = int(sample_rate * chunk_ms / 1000)

        self.logger = get_logger("StreamRecorder")
        self.vad = VoiceActivityDetector()

        self.stream = None

        self.output_dir = (
            Path(__file__).resolve().parent.parent.parent
            / "recordings"
        )
        self.output_dir.mkdir(exist_ok=True)

    # --------------------------------------------------
    # Stream Management
    # --------------------------------------------------

    def start_stream(self):
        """
        Open the microphone if not already open.
        """
        if self.stream is None:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                blocksize=self.chunk_size,
            )
            self.stream.start()
            self.logger.info("Microphone opened")

    def stop_stream(self):
        """
        Close microphone.
        """
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
            self.stream = None
            self.logger.info("Microphone closed")

    # --------------------------------------------------
    # Recording
    # --------------------------------------------------

    def generate_filename(self) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"{timestamp}.wav"

    def record(self) -> Path | None:
        self.logger.info("Listening...")
        self.start_stream()
        buffer = []

        try:
            while True:
                chunk, _ = self.stream.read(self.chunk_size)
                chunk = chunk.flatten()

                state = self.vad.update(chunk)

                if state == "idle":
                    continue

                if state == "start":
                    self.logger.info("Recording started")
                    buffer = [chunk]
                    continue

                if state == "recording":
                    buffer.append(chunk)
                    continue

                if state == "stop":
                    self.logger.info("Recording stopped")
                    if not buffer:
                        return None
                    audio = np.concatenate(buffer)
                    filename = self.generate_filename()
                    sf.write(filename, audio, self.sample_rate)
                    self.logger.info(f"Saved {filename.name}")
                    return filename

        except KeyboardInterrupt:
            self.logger.info("Recording interrupted by user")
            raise
        except Exception as e:
            self.logger.error(f"Error during recording: {e}")
            return None
        finally:
            self.stop_stream()

    # --------------------------------------------------
    # Speech Detection
    # --------------------------------------------------

    def detect_speech(self) -> bool:
        """
        Returns True if speech is detected.
        Used for barge-in / interrupt support.
        """
        self.start_stream()
        chunk, _ = self.stream.read(self.chunk_size)
        chunk = chunk.flatten()
        return self.vad.is_speech(chunk)


if __name__ == "__main__":
    recorder = StreamRecorder()
    print("\nSpeak into microphone...")
    file = recorder.record()
    print(f"Recorded to: {file}")
