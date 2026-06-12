"""Port base: every vendor-facing capability is an ABC here + adapters in core/adapters/.

Business logic imports ports ONLY (Constitution art. 11). Adapter selection is
config-driven. Every adapter must pass its port's conformance suite (conformance.py)
before becoming selectable.
"""
import abc


class Port(abc.ABC):
    """Marker base. Adapters implement a Port subclass; vendor SDK imports live
    only inside adapter modules."""

    vendor: str = "unset"
