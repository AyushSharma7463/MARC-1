from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class AudioFrame:
    """
    One chunk of PCM audio.

    Every component in the audio pipeline
    works with AudioFrame objects.
    """

    samples: np.ndarray
    sample_rate: int
    channels: int
    timestamp: float