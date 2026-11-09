from backend.runtime.component import Component
from backend.runtime.event import Event
from backend.runtime.events import Events

from backend.audio.vad import VoiceActivityDetector


class VAD(Component):
    """
    Voice Activity Detection component.

    Listens:
        audio.frame

    Publishes:
        speech.started
        speech.frame
        speech.ended
    """

    def __init__(self, bus):
        super().__init__("VAD")

        self.bus = bus

        self.detector = VoiceActivityDetector()

    # ---------------------------------

    def start(self):

        self.running = True

        self.bus.subscribe(
            Events.AUDIO_FRAME,
            self.on_audio_frame,
        )

    # ---------------------------------

    def update(self):
        pass

    # ---------------------------------

    def stop(self):

        self.running = False

    # ---------------------------------

    def on_audio_frame(self, event: Event):

        if not self.running:
            return

        frame = event.data["frame"]

        state = self.detector.update(
            frame.samples
        )

        if state == "idle":
            return

        if state == "start":

            self.bus.publish(

                Event(
                    type=Events.SPEECH_STARTED,
                    source=self.name,
                )

            )

            self.bus.publish(

                Event(
                    type=Events.SPEECH_FRAME,
                    source=self.name,
                    data={
                        "frame": frame
                    },
                )

            )

            return

        if state == "recording":

            self.bus.publish(

                Event(
                    type=Events.SPEECH_FRAME,
                    source=self.name,
                    data={
                        "frame": frame
                    },
                )

            )

            return

        if state == "stop":

            self.bus.publish(

                Event(
                    type=Events.SPEECH_ENDED,
                    source=self.name,
                )

            )