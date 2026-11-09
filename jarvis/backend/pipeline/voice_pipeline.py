from backend.audio.stream_recorder import StreamRecorder
from backend.audio.playback_manager import PlaybackManager
from backend.pipeline.assistant import Assistant
from backend.stt.whisper import WhisperSTT
from backend.core.logger import get_logger
from backend.wakeword.detector import WakeWordDetector
from backend.state.conversation import ConversationManager
from backend.runtime.component import Component


class VoicePipeline(Component):
    """
    MARC Voice Pipeline
    """

    def __init__(self):
        super().__init__("voice_pipeline")
        self.logger = get_logger("VoicePipeline")
        self.running = False
        self.event_bus = None

        self.recorder = StreamRecorder()
        self.stt = WhisperSTT()
        self.assistant = Assistant()
        self.wakeword = WakeWordDetector()
        self.conversation = ConversationManager(timeout=20)

        # All audio playback goes through this manager
        self.playback = PlaybackManager()

    # ----------------------------------------
    # Voice Commands
    # ----------------------------------------

    EXIT_COMMANDS = {
        "exit",
        "quit",
        "shutdown",
        "goodbye",
        "stop marc",
    }

    SLEEP_COMMANDS = {
        "sleep",
        "go to sleep",
        "stop listening",
    }

    def update(self, event=None):
        """
        Run one complete voice interaction.
        """

        try:

            # ----------------------------------------
            # Conversation timeout
            # ----------------------------------------
            if (
                self.conversation.is_active()
                and self.conversation.has_timed_out()
            ):
                self.logger.info("Conversation timed out.")

                self.conversation.deactivate()

                print("\nMARC: Going back to sleep.\n")

                self.playback.speak("Going back to sleep.")

                return

            # ----------------------------------------
            # Listen
            # ----------------------------------------
            self.logger.info("Listening for speech...")

            audio_file = self.recorder.record()

            if audio_file is None:
                return

            # ----------------------------------------
            # Speech-to-Text
            # ----------------------------------------
            self.logger.info("Transcribing audio...")

            user_text = self.stt.transcribe(audio_file)

            if not user_text or not user_text.strip():
                return

            print(f"\nYou : {user_text}")

            # Keep original text for the LLM
            original_text = user_text.strip()

            # Normalized version for wake words and commands
            normalized = " ".join(
                original_text.lower().split()
            )

            # ----------------------------------------
            # Sleeping mode
            # ----------------------------------------
            if not self.conversation.is_active():

                activated, cleaned_text = self.wakeword.detect(normalized)

                if not activated:

                    self.logger.info("Wake word not detected.")

                    print("\nWaiting for wake word...\n")

                    return

                self.logger.info("Wake word detected.")

                self.conversation.activate()

                if cleaned_text == "":

                    print("\nMARC: Yes?\n")

                    self.playback.speak("Yes?")

                    return

                normalized = cleaned_text
                original_text = cleaned_text

                print(f"\nCommand : {cleaned_text}")

            else:

                self.logger.info("Conversation active")

                self.conversation.refresh()

            # ----------------------------------------
            # Voice Commands
            # ----------------------------------------
            if normalized in self.EXIT_COMMANDS:

                self.logger.info("Exit command received.")

                self.playback.speak("Shutting down.")

                raise KeyboardInterrupt

            if normalized in self.SLEEP_COMMANDS:

                self.logger.info("Sleep command received.")

                self.conversation.deactivate()

                self.playback.speak("Going back to sleep.")

                return

            # ----------------------------------------
            # Assistant
            # ----------------------------------------
            self.logger.info("Generating response...")

            response = self.assistant.chat(user_text)

            if not response:
              return

            print(f"\nMARC: {response}")

# Speak the response (blocking until speech is finished)
            self.playback.speak(response)

# NOW restart the conversation timeout
            self.conversation.refresh()


            print("\n----------------------------------------")

        except KeyboardInterrupt:

            self.logger.info("Interrupted by user.")

            raise

        except Exception as e:
            self.logger.exception(f"Voice pipeline failed: {e}")

    def run(self):
        """
        Run one voice interaction cycle (alias for update).
        """
        return self.update()

    def start(self):
        self.running = True
        self.logger.info("VoicePipeline started")

    def stop(self):
        self.running = False
        self.logger.info("VoicePipeline stopped")
