from threading import Lock, Thread

from backend.core.logger import get_logger
from backend.core.settings import settings
from backend.tts.piper import PiperTTS


class PlaybackManager:
    """
    Controls all speech playback for MARC.

    Features
    --------
    - Thread-safe playback
    - Non-blocking speech
    - Interrupt support
    - Optional Shared AudioState integration
    """

    def __init__(self, model_path: str | None = None, audio_state=None):
        self.logger = get_logger("PlaybackManager")
        self.audio_state = audio_state

        effective_model = model_path or settings.PIPER_MODEL
        self.tts = PiperTTS(model_path=effective_model)

        self._lock = Lock()
        self._thread = None

    # --------------------------------------------------
    # Blocking playback
    # --------------------------------------------------

    def speak(self, text: str):
        """
        Blocking speech.
        """
        if not text or not text.strip():
            return

        with self._lock:
            if self.audio_state:
                self.audio_state.start_speaking()

            self.logger.info("Playback started")

            try:
                self.tts.speak(text)
            finally:
                if self.audio_state:
                    self.audio_state.stop_speaking()

                self._thread = None
                self.logger.info("Playback finished")

    # --------------------------------------------------
    # Background playback
    # --------------------------------------------------

    def speak_async(self, text: str):
        """
        Speak in a background thread.
        """
        if not text or not text.strip():
            return

        if self.is_playing():
            self.logger.warning("Playback already in progress.")
            return

        self._thread = Thread(
            target=self.speak,
            args=(text,),
            daemon=True,
            name="PlaybackThread",
        )
        self._thread.start()

    # --------------------------------------------------
    # Stop playback
    # --------------------------------------------------

    def stop(self):
        """
        Interrupt current playback.
        """
        if self.tts.is_playing():
            self.logger.info("Playback interrupted")
            self.tts.stop()

        if self.audio_state:
            self.audio_state.stop_speaking()

    # --------------------------------------------------
    # Wait for playback
    # --------------------------------------------------

    def wait(self):
        """
        Wait until playback finishes.
        """
        thread = self._thread
        if thread is not None:
            thread.join()
            self._thread = None

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def is_playing(self) -> bool:
        """
        Returns True while speech is playing.
        """
        return self.tts.is_playing()
