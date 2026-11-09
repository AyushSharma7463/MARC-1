from backend.audio.runtime.audio_state import AudioState
from backend.core.logger import get_logger
from backend.runtime.component import Component
from backend.runtime.event import Event
from backend.runtime.events import Events


class InterruptManager(Component):
    """
    Detects spoken interrupt commands while MARC is speaking.

    Listens:
        text.transcribed

    Publishes:
        interrupt
    """

    INTERRUPT_WORDS = {
        "stop",
        "cancel",
        "pause",
        "quiet",
        "be quiet",
        "enough",
        "silence",
        "shut up",
    }

    def __init__(
        self,
        bus,
        audio_state: AudioState,
    ):
        super().__init__("InterruptManager")

        self.bus = bus
        self.audio_state = audio_state
        self.logger = get_logger("InterruptManager")

    # --------------------------------------------------

    def start(self):
        self.running = True
        self.bus.subscribe(
            Events.TEXT_TRANSCRIBED,
            self.on_transcription,
        )

    # --------------------------------------------------

    def update(self):
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

        # Ignore if MARC isn't speaking
        if not self.audio_state.speaking:
            return

        text = event.data.get("text", "").lower().strip()
        if not text:
            return

        for phrase in self.INTERRUPT_WORDS:
            if phrase in text:
                self.logger.info(f"Interrupt detected: {phrase}")
                self.audio_state.interrupted = True

                self.bus.publish(
                    Event(
                        type=Events.INTERRUPT,
                        source=self.name,
                        data={
                            "command": phrase,
                            "text": text,
                        },
                    )
                )
                return
