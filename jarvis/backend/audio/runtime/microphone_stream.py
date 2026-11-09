import time

import sounddevice as sd

from backend.audio.runtime.audio_frame import AudioFrame
from backend.core.logger import get_logger


class MicrophoneStream:
    """
    Continuous microphone stream.

    Produces one AudioFrame for each read().
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

        self.chunk_size = int(
            sample_rate * chunk_ms / 1000
        )

        self.logger = get_logger("MicrophoneStream")

        self.stream = None

    # -------------------------------------------------

    def start(self):

        if self.stream is not None:
            return

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            blocksize=self.chunk_size,
        )

        self.stream.start()

        self.logger.info("Microphone opened")

    # -------------------------------------------------

    def stop(self):

        if self.stream is None:
            return

        self.stream.stop()
        self.stream.close()

        self.stream = None

        self.logger.info("Microphone closed")

    # -------------------------------------------------

    def read(self) -> AudioFrame | None:

        if self.stream is None:
            return None

        samples, _ = self.stream.read(self.chunk_size)

        return AudioFrame(
            samples=samples.flatten(),
            sample_rate=self.sample_rate,
            channels=self.channels,
            timestamp=time.time(),
        )