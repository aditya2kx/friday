"""SpeakerID port — enroll and identify speakers for voice auth."""
from .base import Port
import abc


class SpeakerID(Port):
    """Abstraction over speaker identification backends (e.g. Picovoice Eagle, pyannote)."""

    @abc.abstractmethod
    def enroll(self, name: str, samples: list[bytes]) -> None:
        """Enroll a speaker with audio samples."""
        ...

    @abc.abstractmethod
    def identify(self, audio: bytes) -> tuple[str | None, float]:
        """Identify speaker from audio. Returns (name_or_None, confidence_score)."""
        ...
