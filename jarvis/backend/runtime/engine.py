import time

from backend.core.logger import get_logger


class Engine:
    """
    MARC Runtime Engine

    Responsibilities
    ----------------
    - Register runtime components
    - Manage lifecycle
    - Execute the runtime loop

    The Engine contains no AI logic.
    """

    def __init__(self, bus):

        self.logger = get_logger("Engine")

        self.bus = bus

        self.components = []

        self.running = False

    # -------------------------------------------------
    # Component Management
    # -------------------------------------------------

    def register(self, component):
        """
        Register a runtime component.
        """

        self.components.append(component)

        self.logger.info(
            f"Registered component: {component.name}"
        )

    # -------------------------------------------------
    # Lifecycle
    # -------------------------------------------------

    def start(self):
        """
        Start every registered component.
        """

        self.logger.info("Starting MARC Engine...")

        self.running = True

        for component in self.components:

            try:
                component.start()

            except Exception as e:

                self.logger.exception(
                    f"Failed to start '{component.name}': {e}"
                )

        self.logger.info("Engine started successfully.")

    # -------------------------------------------------

    def run(self):
        """
        Main runtime loop.

        Every component gets one update every tick.
        """

        self.logger.info("Engine running...")

        while self.running:

            try:

                for component in self.components:

                    component.update()

                # ~200 FPS runtime tick
                time.sleep(0.005)

            except KeyboardInterrupt:

                self.logger.info("Shutdown requested.")

                self.stop()

            except Exception as e:

                self.logger.exception(
                    f"Engine crash: {e}"
                )

                self.stop()

    # -------------------------------------------------

    def stop(self):
        """
        Stop every component safely.
        """

        if not self.running:
            return

        self.logger.info("Stopping MARC Engine...")

        self.running = False

        for component in reversed(self.components):

            try:

                component.stop()

            except Exception as e:

                self.logger.exception(
                    f"Failed stopping '{component.name}': {e}"
                )

        self.logger.info("Engine stopped.")