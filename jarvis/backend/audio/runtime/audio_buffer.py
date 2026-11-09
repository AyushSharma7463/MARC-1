from __future__ import annotations

from typing import List
import numpy as np

from backend.audio.runtime.audio_frame import AudioFrame


class AudioBuffer:
    """
    Collects AudioFrames belonging to one speech segment.

    Lifecycle:

        start()
            ↓
        append()
            ↓
        append()
            ↓
        append()
            ↓
        finish()
    """

    def __init__(self):

        self.frames: List[AudioFrame] = []

        self.active = False

    # ---------------------------------

    def start(self):

        self.frames.clear()

        self.active = True

    # ---------------------------------

    def append(self, frame: AudioFrame):

        if not self.active:
            return

        self.frames.append(frame)

    # ---------------------------------

    def finish(self):

        if not self.frames:

            self.active = False

            return None

        audio = np.concatenate(

            [frame.samples for frame in self.frames]

        )

        sample_rate = self.frames[0].sample_rate

        channels = self.frames[0].channels

        self.clear()

        return {

            "samples": audio,

            "sample_rate": sample_rate,

            "channels": channels,

        }

    # ---------------------------------

    def clear(self):

        self.frames.clear()

        self.active = False