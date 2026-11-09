from backend.runtime.component import Component
from backend.runtime.event import Event
from backend.runtime.events import Events

from backend.audio.runtime.microphone_stream import MicrophoneStream
from backend.audio.runtime.audio_state import AudioState


class Microphone(Component):
    """
    Continuous microphone component.

    Responsibilities
    ----------------
    - Own the microphone stream
    - Continuously read AudioFrames
    - Publish audio.frame events

    It does NOT:
    - Perform VAD
    - Save WAV files
    - Call Whisper
    """

    def __init__(self, bus, audio_state: AudioState):
        super().__init__("Microphone")

        self.bus = bus
        self.audio_state = audio_state

        self.stream = MicrophoneStream()

    # --------------------------------------------------

    def start(self):
        self.running = True
        self.stream.start()

    # --------------------------------------------------

    def update(self):

        if not self.running:
            return

        frame = self.stream.read()

        if frame is None:
            return

        self.bus.publish(

            Event(
                type=Events.AUDIO_FRAME,
                source=self.name,
                data={
                    "frame": frame
                },
            )

        )

    # --------------------------------------------------

    def stop(self):

        self.running = False

        self.stream.stop()