"""IntakeConnector port — normalize inbound signals into work items."""
from .base import Port
import abc


class IntakeConnector(Port):
    """Abstraction over intake surfaces (e.g. Slack, voice memos, email)."""

    @abc.abstractmethod
    def normalize(self, event: dict) -> dict:
        """Normalize a raw inbound event to {title, body, source, thread_ref, priority}."""
        ...

    @abc.abstractmethod
    def reply(self, thread_ref: str, message: str) -> None:
        """Send a reply back to the originating thread."""
        ...
