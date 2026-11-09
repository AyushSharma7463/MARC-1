from __future__ import annotations

import numpy as np

from backend.runtime.component import Component
from backend.runtime.event import Event
from backend.runtime.events import Events


class AudioBuffer(Component):
    """
    Collects speech frames into one audio segment.

    Listens:
        speech.started
        speech.frame
        speech.ended

    Publishes:
        audio.segment
    """

    def __init__(self, bus):
        super().__init__("AudioBuffer")

        self.bus = bus

        self.frames = []

        self.sample_rate = 16000

        self.channels = 1

    # ---------------------------------

    def start(self):

        self.running = True

        self.bus.subscribe(
            Events.SPEECH_STARTED,
            self.on_started,
        )

        self.bus.subscribe(
            Events.SPEECH_FRAME,
            self.on_frame,
        )

        self.bus.subscribe(
            Events.SPEECH_ENDED,
            self.on_ended,
        )

    # ---------------------------------

    def update(self):
        pass

    # ---------------------------------

    def stop(self):

        self.running = False

        self.frames.clear()

    # ---------------------------------

    def on_started(self, event: Event):

        self.frames.clear()

    # ---------------------------------

    def on_frame(self, event: Event):

        frame = event.data["frame"]

        self.sample_rate = frame.sample_rate
        self.channels = frame.channels

        self.frames.append(frame.samples)

    # ---------------------------------

    def on_ended(self, event: Event):

        if not self.frames:
            return

        audio = np.concatenate(self.frames)

        self.bus.publish(

            Event(
                type=Events.AUDIO_SEGMENT,
                source=self.name,
                data={
                    "audio": audio,
                    "sample_rate": self.sample_rate,
                    "channels": self.channels,
                },
            )

        )

        self.frames.clear()