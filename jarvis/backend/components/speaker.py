from backend.runtime.component import Component
from backend.runtime.event import Event
from backend.runtime.events import Events

from backend.audio.playback_manager import PlaybackManager
from backend.audio.runtime.audio_state import AudioState

from backend.core.logger import get_logger
from backend.core.settings import settings


class Speaker(Component):
    """
    Speaker component.

    Listens:
        response.generated

    Speaks assistant responses.
    """

    def __init__(
        self,
        bus,
        audio_state: AudioState,
    ):
        super().__init__("Speaker")

        self.bus = bus
        self.audio_state = audio_state

        self.logger = get_logger("Speaker")

        self.tts = PlaybackManager(
            model_path=settings.PIPER_MODEL,
            audio_state=audio_state,
        )

    # --------------------------------------------------

    def start(self):
        self.running = True

        self.bus.subscribe(
            Events.RESPONSE_GENERATED,
            self.on_response,
        )

        self.bus.subscribe(
            Events.INTERRUPT,
            self.on_interrupt,
        )

    # --------------------------------------------------

    def update(self):
        pass

    # --------------------------------------------------

    def stop(self):
        self.running = False

        self.bus.unsubscribe(
            Events.RESPONSE_GENERATED,
            self.on_response,
        )

        self.bus.unsubscribe(
            Events.INTERRUPT,
            self.on_interrupt,
        )

        self.tts.stop()

    # --------------------------------------------------

    def on_response(self, event: Event):

        if not self.running:
            return

        text = event.data.get("text", "").strip()

        if not text:
            return

        self.logger.info(f"MARC: {text}")

        self.tts.speak_async(text)

    # --------------------------------------------------

    def on_interrupt(self, event: Event):

        self.logger.info("Stopping speech")

        self.tts.stop()

        self.audio_state.stop_speaking()