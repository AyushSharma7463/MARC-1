class AudioState:
    """
    Shared audio state for full duplex control
    """

    def __init__(self):
        self.is_speaking = False
        self.is_listening = True
        self.should_interrupt_tts = False

    def start_speaking(self):
        self.is_speaking = True
        self.is_listening = False

    def stop_speaking(self):
        self.is_speaking = False
        self.is_listening = True

    def interrupt(self):
        self.should_interrupt_tts = True

    def reset_interrupt(self):
        self.should_interrupt_tts = False