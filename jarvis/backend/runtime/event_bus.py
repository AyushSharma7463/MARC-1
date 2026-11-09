from __future__ import annotations

from collections import defaultdict
from queue import Queue
from threading import Thread
from typing import Callable

from backend.core.logger import get_logger
from backend.runtime.event import Event


class EventBus:
    """
    Asynchronous Event Bus.

    Publishers never call handlers directly.

    Events are placed into a queue and processed
    by a dedicated worker thread.
    """

    def __init__(self):

        self.logger = get_logger("EventBus")

        self.subscribers = defaultdict(list)

        self.queue = Queue()

        self.running = True

        self.worker = Thread(
            target=self._worker,
            daemon=True,
            name="EventBusWorker",
        )

        self.worker.start()

    # ---------------------------------

    def subscribe(
        self,
        event_type: str,
        handler: Callable,
    ):

        self.subscribers[event_type].append(handler)

        self.logger.info(
            f"Subscribed {handler.__qualname__} -> {event_type}"
        )

    # ---------------------------------

    def unsubscribe(
        self,
        event_type: str,
        handler: Callable,
    ):

        if handler in self.subscribers[event_type]:

            self.subscribers[event_type].remove(handler)

    # ---------------------------------

    def publish(self, event: Event):
        """
        Non-blocking.

        Simply enqueue the event.
        """

        self.queue.put(event)

    # ---------------------------------

    def _worker(self):

        while self.running:

            event = self.queue.get()

            handlers = self.subscribers.get(
                event.type,
                [],
            )

            if not handlers:

                continue

            for handler in handlers:

                try:

                    handler(event)

                except Exception:

                    self.logger.exception(
                        f"Handler failed: {event.type}"
                    )

    # ---------------------------------

    def stop(self):

        self.running = False