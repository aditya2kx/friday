"""ReviewBot port — automated PR review."""
from .base import Port
import abc


class ReviewBot(Port):
    """Abstraction over automated review backends (e.g. Claude, GPT, custom)."""

    @abc.abstractmethod
    def review(self, pr_ref: str, rubric: str) -> list[dict]:
        """Review a PR against a rubric. Returns list of comment dicts."""
        ...
