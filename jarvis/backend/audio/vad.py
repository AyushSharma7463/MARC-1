import numpy as np

try:
    from backend.core.logger import get_logger
except ModuleNotFoundError:
    # Allow running this file directly
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    sys.path.append(str(project_root))

    from backend.core.logger import get_logger


class VoiceActivityDetector:
    """
    Energy-based Voice Activity Detection (VAD).

    States:
        - Idle
        - Speech Detected
        - Recording
        - Stop Recording
    """

    def __init__(
        self,
        threshold: float = 0.008,
        speech_frames: int = 1,
        silence_frames: int = 50,
    ):
        """
        Parameters
        ----------
        threshold
            Minimum RMS energy considered speech.

        speech_frames
            Number of consecutive speech chunks required
            before recording starts.

        silence_frames
            Number of consecutive silence chunks required
            before recording stops.
        """

        self.threshold = threshold

        self.required_speech_frames = speech_frames
        self.required_silence_frames = silence_frames

        self.speech_count = 0
        self.silence_count = 0

        self.recording = False

        self.logger = get_logger("VAD")

    def rms(self, audio_chunk: np.ndarray) -> float:
        """
        Compute RMS energy.
        """

        if len(audio_chunk) == 0:
            return 0.0

        return np.sqrt(np.mean(audio_chunk ** 2))

    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        """
        Returns True if the audio chunk contains speech.
        """

        energy = self.rms(audio_chunk)

        self.logger.info(f"Energy: {energy:.5f}")

        return energy >= self.threshold

    def update(self, audio_chunk: np.ndarray):
        """
        Process one audio chunk.

        Returns
        -------
        idle
            Waiting for speech.

        start
            Start recording.

        recording
            Continue recording.

        stop
            Stop recording.
        """

        is_speech = self.is_speech(audio_chunk)

        # -----------------------------
        # Waiting for speech
        # -----------------------------
        if not self.recording:

            if is_speech:

                self.speech_count += 1

                if self.speech_count >= self.required_speech_frames:

                    self.recording = True
                    self.silence_count = 0

                    self.logger.info("Speech detected")

                    return "start"

            else:

                self.speech_count = 0

            return "idle"

        # -----------------------------
        # Already recording
        # -----------------------------
        if is_speech:

            self.silence_count = 0

            return "recording"

        self.silence_count += 1

        if self.silence_count >= self.required_silence_frames:

            self.recording = False

            self.speech_count = 0
            self.silence_count = 0

            self.logger.info("Silence detected")

            return "stop"

        return "recording"