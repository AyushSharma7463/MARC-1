from abc import ABC, abstractmethod


class Component(ABC):
    """
    Base Component for MARC v2

    Every system module must follow this lifecycle:
    - start()
    - update()
    - stop()
    """

    def __init__(self, name: str):
        self.name = name
        self.running = False

    # ------------------------------------
    # Lifecycle Methods
    # ------------------------------------

    @abstractmethod
    def start(self):
        """
        Called once when engine starts.
        """
        self.running = True

    @abstractmethod
    def update(self):
        """
        Called repeatedly by engine loop.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Called when engine shuts down.
        """
        self.running = False