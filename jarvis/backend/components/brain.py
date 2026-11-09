from backend.runtime.component import Component
from backend.runtime.event import Event
from backend.brain.orchestrator import Orchestrator


class Brain(Component):
    """
    Event-driven reasoning core.
    """

    def __init__(self, bus):
        super().__init__("brain")

        self.bus = bus
        self.orchestrator = Orchestrator()

    def start(self):
        self.running = True

        # CRITICAL: subscribe to input events
        self.bus.subscribe("text.recognized", self.on_text)

    def update(self):
        # No polling needed in event-driven design
        pass

    def stop(self):
        self.running = False

    def on_text(self, event: Event):
        if not self.running:
            return

        text = event.data.get("text")
        if not text:
            return

        # Step 1: decide
        result = self.orchestrator.process(text)

        # Step 3: publish response
        self.bus.publish(
            Event(
                type="response.generated",
                data={"text": result},
                source=self.name
            )
        )