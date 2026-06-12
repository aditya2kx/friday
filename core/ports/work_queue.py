"""WorkQueue port — issue/task backlog management."""
from .base import Port
import abc


class WorkQueue(Port):
    """Abstraction over issue/task queue backends (e.g. GitHub Issues, Linear)."""

    @abc.abstractmethod
    def file(self, title, body, labels) -> str:
        """File a new item. Returns item_ref."""
        ...

    @abc.abstractmethod
    def update(self, item_ref, **fields) -> None:
        """Update fields on an existing item."""
        ...

    @abc.abstractmethod
    def transition(self, item_ref, state) -> None:
        """Move an item to a new state (e.g. triage → ready → in-progress)."""
        ...

    @abc.abstractmethod
    def query(self, **filters) -> list[dict]:
        """Return items matching filters."""
        ...
