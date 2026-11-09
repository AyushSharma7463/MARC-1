from __future__ import annotations

from threading import Lock


class AudioState:
    """
    Shared runtime audio state.

    Every component receives the same instance.
    """

    def __init__(self):

        self._lock = Lock()

        self.listening = True
        self.speaking = False
        self.generating = False
        self.interrupted = False
        self.wake_detected = False

    # -------------------------

    def start_speaking(self):
        with self._lock:
            self.speaking = True

    def stop_speaking(self):
        with self._lock:
            self.speaking = False

    # -------------------------

    def start_generation(self):
        with self._lock:
            self.generating = True

    def stop_generation(self):
        with self._lock:
            self.generating = False

    # -------------------------

    def interrupt(self):
        with self._lock:
            self.interrupted = True

    def clear_interrupt(self):
        with self._lock:
            self.interrupted = False