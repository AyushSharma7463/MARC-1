from pathlib import Path
import time

from faster_whisper import WhisperModel

from backend.core.logger import get_logger


class WhisperSTT:
    """
    Speech-to-Text using Faster-Whisper.

    Optimized for a real-time voice assistant.
    """

    def __init__(
        self,
        model_size: str = "base",
        device: str = "auto",
        compute_type: str = "int8",
    ):
        self.logger = get_logger("Whisper")

        self.logger.info("Loading Faster-Whisper model...")

        start = time.time()

        self.model = WhisperModel(
            model_size_or_path=model_size,
            device=device,
            compute_type=compute_type,
        )

        elapsed = time.time() - start

        self.logger.info(
            f"Whisper model loaded in {elapsed:.2f}s"
        )

    def transcribe(self, audio_path: str | Path) -> str:
        """
        Transcribe a WAV audio file.
        """

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        self.logger.info(
            f"Transcribing {audio_path.name}"
        )

        start = time.time()

        segments, info = self.model.transcribe(
             str(audio_path),

    # Fastest decoding
      beam_size=1,
     best_of=1,

    # Fixed language
     language="en",

    # Not needed for a voice assistant
    word_timestamps=False,

    # Prevent previous context from affecting the result
    condition_on_previous_text=False,
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        elapsed = time.time() - start

        self.logger.info(
            f"Language: {info.language}"
        )

        self.logger.info(
            f"Transcription completed in {elapsed:.2f}s"
        )

        return text


if __name__ == "__main__":

    audio_file = (
        Path(__file__).resolve().parent.parent.parent
        / "recordings"
        / "output.wav"
    )

    stt = WhisperSTT()

    print("\nTranscribing...\n")

    result = stt.transcribe(audio_file)

    print("\nYou said:")
    print(result)