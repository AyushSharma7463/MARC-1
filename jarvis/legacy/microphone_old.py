import numpy as np
import sounddevice as sd
from backend.core.logger import get_logger


class Microphone:
    """
    Legacy standalone microphone helper for Jarvis.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        device: int | None = None,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device
        self.logger = get_logger("Microphone")

    def list_devices(self):
        """
        Print and return all available audio devices.
        """
        devices = sd.query_devices()
        for index, device in enumerate(devices):
            self.logger.info(f"{index}: {device['name']}")
        return devices

    def record(self, duration: float) -> np.ndarray:
        """
        Record audio from the microphone for a given duration in seconds.
        """
        frames = int(duration * self.sample_rate)
        self.logger.info(f"Recording {duration}s from mic...")
        recording = sd.rec(
            frames,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            device=self.device,
        )
        sd.wait()
        return recording.squeeze()
