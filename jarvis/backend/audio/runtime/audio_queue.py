from queue import Queue


class AudioQueue:
    """
    Thread-safe queue for audio frames.
    """

    def __init__(self):
        self.queue = Queue()

    def push(self, frame):
        self.queue.put(frame)

    def pop(self):
        return self.queue.get()

    def empty(self):
        return self.queue.empty()