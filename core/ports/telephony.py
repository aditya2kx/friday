"""Telephony port — phone call handling for voice access from any phone."""
from .base import Port
import abc


class Telephony(Port):
    """Abstraction over telephony backends (e.g. Twilio, Vonage)."""

    @abc.abstractmethod
    def on_call(self, handler) -> None:
        """Register a handler for incoming calls."""
        ...

    @abc.abstractmethod
    def audio_bridge(self, call_ref):
        """Return a duplex stream handle for a call's audio."""
        ...
