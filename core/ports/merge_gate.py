"""MergeGate port — manage PRs in a merge queue."""
from .base import Port
import abc


class MergeGate(Port):
    """Abstraction over merge queue backends (e.g. GitHub merge queue, Mergify)."""

    @abc.abstractmethod
    def enter(self, pr_ref) -> None:
        """Add a PR to the merge queue."""
        ...

    @abc.abstractmethod
    def eject(self, pr_ref, reason) -> None:
        """Remove a PR from the merge queue with a reason."""
        ...

    @abc.abstractmethod
    def position(self, pr_ref) -> int | None:
        """Return queue position of a PR (None if not in queue)."""
        ...
