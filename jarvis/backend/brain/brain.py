from backend.runtime.component import Component
from backend.runtime.event import Event
from backend.runtime.events import Events

from backend.audio.runtime.audio_state import AudioState
from backend.brain.orchestrator import Orchestrator

from backend.core.logger import get_logger


class Brain(Component):
    """
    MARC Brain

    Listens:
        text.transcribed

    Publishes:
        response.generated
    """

    def __init__(
        self,
        bus,
        audio_state: AudioState,
    ):
        super().__init__("Brain")

        self.bus = bus
        self.audio_state = audio_state

        self.logger = get_logger("Brain")

        self.orchestrator = Orchestrator()

    # --------------------------------------------------

    def start(self):

        self.running = True

        self.bus.subscribe(
            Events.TEXT_TRANSCRIBED,
            self.on_transcription,
        )

    # --------------------------------------------------

    def update(self):
        """
        Event-driven component.
        """
        pass

    # --------------------------------------------------

    def stop(self):

        self.running = False

        self.bus.unsubscribe(
            Events.TEXT_TRANSCRIBED,
            self.on_transcription,
        )

    # --------------------------------------------------

    def on_transcription(self, event: Event):

        if not self.running:
            return

        text = event.data.get("text", "").strip()

        if not text:
            return

        # Ignore user requests while an interrupt is active
        if self.audio_state.interrupted:
            self.audio_state.interrupted = False
            return

        self.logger.info(f"User: {text}")

        self.audio_state.generating = True

        try:
            response = self.orchestrator.process(text)

            if not response:
                return

            self.logger.info(f"MARC: {response}")

            self.bus.publish(
                Event(
                    type=Events.RESPONSE_GENERATED,
                    source=self.name,
                    data={
                        "text": response,
                    },
                )
            )

        finally:
            self.audio_state.generating = False