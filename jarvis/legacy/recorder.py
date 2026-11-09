from pathlib import Path

import soundfile as sf

try:
    from legacy.microphone_old import Microphone
except ModuleNotFoundError:
    try:
        from jarvis.legacy.microphone_old import Microphone
    except ModuleNotFoundError:
        from microphone_old import Microphone
from backend.core.logger import get_logger

class Recorder:
    """
    Records audio from the microphone and saves it as a WAV file.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
    ):
        self.microphone = Microphone(
            sample_rate=sample_rate,
            channels=channels,
        )

        self.sample_rate = sample_rate

        self.logger = get_logger("Recorder")

        # Always save inside the project's recordings folder
        self.output_dir = (
            Path(__file__).resolve().parent.parent.parent / "recordings"
        )
        self.output_dir.mkdir(exist_ok=True)

    def record(
        self,
        duration: float = 5,
        filename: str = "output.wav",
    ) -> Path:
        """
        Record audio and save it as a WAV file.

        Returns
        -------
        Path
            Path to the saved recording.
        """

        self.logger.info("Starting recorder")

        audio = self.microphone.record(duration)

        output_path = self.output_dir / filename

        sf.write(
            output_path,
            audio,
            self.sample_rate,
        )

        self.logger.info(f"Audio saved to {output_path}")

        return output_path


if __name__ == "__main__":
    recorder = Recorder()

    print("Recording for 5 seconds...")

    file_path = recorder.record()

    print(f"\nRecording saved to:\n{file_path}")