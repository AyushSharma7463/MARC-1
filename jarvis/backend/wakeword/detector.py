import re


class WakeWordDetector:
    """
    Detects wake words and removes them
    from the beginning of the user's speech.
    """

    WAKE_WORDS = (
        "jarvis",
        "hello jarvis",
        "hi jarvis",
        "ok jarvis",
        "okay jarvis",
        "hey jarvis",
        "hey marc",
        "marc",
        "hey",
    )

    def detect(self, text: str) -> tuple[bool, str]:
        """
        Returns
        -------
        (activated, cleaned_text)
        """

        if not text:
            return False, ""

        text = self._normalize(text)

        for wake_word in sorted(
            self.WAKE_WORDS,
            key=len,
            reverse=True,
        ):

            if text.startswith(wake_word):

                cleaned = text[len(wake_word):].strip()

                return True, cleaned

        return False, text

    @staticmethod
    def _normalize(text: str) -> str:

        text = text.lower()

        text = re.sub(r"[^\w\s]", "", text)

        text = " ".join(text.split())

        return text