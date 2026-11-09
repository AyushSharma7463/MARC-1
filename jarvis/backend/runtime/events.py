"""
backend/runtime/events.py

Central registry of all runtime event names.

Every component should import Events instead of
hardcoding event names.
"""


class Events:
    # ==================================================
    # Audio Pipeline
    # ==================================================

    AUDIO_FRAME = "audio.frame"

    SPEECH_STARTED = "speech.started"

    SPEECH_FRAME = "speech.frame"

    SPEECH_ENDED = "speech.ended"

    AUDIO_SEGMENT = "audio.segment"

    # ==================================================
    # Speech Recognition
    # ==================================================

    TEXT_TRANSCRIBED = "text.transcribed"

    # ==================================================
    # Brain
    # ==================================================

    RESPONSE_GENERATED = "response.generated"

    # ==================================================
    # Runtime
    # ==================================================

    INTERRUPT = "interrupt"

    WAKE_WORD = "wakeword.detected"

    ERROR = "runtime.error"

    # ==================================================
    # Optional Runtime Events (recommended)
    # ==================================================

    ENGINE_STARTED = "engine.started"

    ENGINE_STOPPED = "engine.stopped"

    PLAYBACK_STARTED = "playback.started"

    PLAYBACK_FINISHED = "playback.finished"

    PLAYBACK_STOPPED = "playback.stopped"

    MICROPHONE_STARTED = "microphone.started"

    MICROPHONE_STOPPED = "microphone.stopped"

    WHISPER_STARTED = "whisper.started"

    WHISPER_FINISHED = "whisper.finished"

    BRAIN_STARTED = "brain.started"

    BRAIN_FINISHED = "brain.finished"

    SKILL_STARTED = "skill.started"

    SKILL_FINISHED = "skill.finished"

    WAKEWORD_STARTED = "wakeword.started"

    WAKEWORD_DETECTED = "wakeword.detected"

    LOG = "runtime.log"