from __future__ import annotations

import tempfile
from pathlib import Path

import soundfile as sf

from backend.runtime.component import Component
from backend.runtime.event import Event
from backend.runtime.events import Events

from backend.stt.whisper import WhisperSTT


class Whisper(Component):
    """
    Runtime Speech-to-Text component.

    Listens:
        audio.segment

    Publishes:
        text.transcribed
    """

    def __init__(self, bus):
        super().__init__("Whisper")

        self.bus = bus

        self.model = WhisperSTT()

    # ---------------------------------

    def start(self):

        self.running = True

        self.bus.subscribe(
            Events.AUDIO_SEGMENT,
            self.on_audio_segment,
        )

    # ---------------------------------

    def update(self):
        pass

    # ---------------------------------

    def stop(self):

        self.running = False

    # ---------------------------------

    def on_audio_segment(self, event: Event):

        if not self.running:
            return

        audio = event.data["audio"]

        sample_rate = event.data["sample_rate"]

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as tmp:

            temp_path = Path(tmp.name)

        try:

            sf.write(
                temp_path,
                audio,
                sample_rate,
            )

            text = self.model.transcribe(
                temp_path
            )

            if not text:
                return

            self.bus.publish(

                Event(
                    type=Events.TEXT_TRANSCRIBED,
                    source=self.name,
                    data={
                        "text": text
                    },
                )

            )

        finally:

            temp_path.unlink(
                missing_ok=True
            )