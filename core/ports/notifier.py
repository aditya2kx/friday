"""Notifier port — send messages to operator channels."""
from .base import Port
import abc


class Notifier(Port):
    """Abstraction over notification backends (e.g. Slack, SMS, push)."""

    @abc.abstractmethod
    def send(self, channel_ref: str, message: str, blocks: list | None = None) -> None:
        """Send a message to a channel."""
        ...
