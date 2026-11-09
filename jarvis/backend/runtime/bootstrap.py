from backend.runtime.engine import Engine
from backend.runtime.event_bus import EventBus

from backend.audio.runtime.audio_state import AudioState

from backend.components.microphone import Microphone
from backend.components.vad import VAD
from backend.components.audio_buffer import AudioBuffer
from backend.components.whisper import Whisper
from backend.components.interrupt_manager import InterruptManager
from backend.components.speaker import Speaker

from backend.brain.brain import Brain


def build_system() -> Engine:
    """
    Build and wire the MARC runtime.
    """

    # --------------------------------------------------
    # Shared Runtime Objects
    # --------------------------------------------------

    bus = EventBus()

    audio_state = AudioState()

    # --------------------------------------------------
    # Engine
    # --------------------------------------------------

    engine = Engine(bus)

    # --------------------------------------------------
    # Runtime Components
    # --------------------------------------------------

    engine.register(
        Microphone(
            bus=bus,
            audio_state=audio_state,
        )
    )

    engine.register(
        VAD(bus)
    )

    engine.register(
        AudioBuffer(bus)
    )

    engine.register(
        Whisper(bus)
    )

    engine.register(
        InterruptManager(
            bus=bus,
            audio_state=audio_state,
        )
    )

    engine.register(
        Brain(
            bus=bus,
            audio_state=audio_state,
        )
    )

    engine.register(
        Speaker(
            bus=bus,
            audio_state=audio_state,
        )
    )

    return engine