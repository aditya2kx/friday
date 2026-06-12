"""VoiceEngine port — real-time voice I/O sessions."""
from .base import Port
import abc


class VoiceEngine(Port):
    """Abstraction over voice AI backends (e.g. OpenAI Realtime, Gemini Live, Vapi)."""

    @abc.abstractmethod
    def open_session(self, tools: list[dict]) -> str:
        """Open a voice session with the given tool definitions. Returns session_ref."""
        ...

    @abc.abstractmethod
    def send_audio(self, session_ref, chunk: bytes) -> None:
        """Send an audio chunk to an open session."""
        ...

    @abc.abstractmethod
    def events(self, session_ref):
        """Iterate events from an open session (iterator of dicts)."""
        ...

    @abc.abstractmethod
    def close(self, session_ref) -> None:
        """Close an open session."""
        ...
