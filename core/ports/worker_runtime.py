"""WorkerRuntime port — launch and steer autonomous dev workers."""
from .base import Port
import abc


class WorkerRuntime(Port):
    """Abstraction over worker execution platforms (e.g. Cursor Cloud, Devin, local)."""

    @abc.abstractmethod
    def launch(self, issue_ref: str, scope: list[str], budget_usd: float) -> str:
        """Launch a worker for the given issue. Returns a run_ref."""
        ...

    @abc.abstractmethod
    def steer(self, run_ref: str, message: str) -> None:
        """Send a steering message to a running worker."""
        ...

    @abc.abstractmethod
    def status(self, run_ref: str) -> dict:
        """Return current status of a worker run."""
        ...
