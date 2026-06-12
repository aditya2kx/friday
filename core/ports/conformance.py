"""Conformance harness: each port defines a suite of contract tests an adapter
must pass before it is selectable. M0 ships the harness; suites fill in as
adapters arrive (M2+)."""


class ConformanceSuite:
    port_cls = None  # set by subclass

    def run(self, adapter) -> dict:
        assert self.port_cls is not None
        assert isinstance(adapter, self.port_cls), (
            f"{adapter!r} does not implement {self.port_cls.__name__}")
        return {"port": self.port_cls.__name__, "vendor": adapter.vendor, "passed": True}
