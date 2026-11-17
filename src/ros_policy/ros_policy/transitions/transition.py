from __future__ import annotations

from ..behaviors import Behavior


class Transition:
    """A condition to enable the passage from one behavior to another."""
    origin: Behavior = None
    target: Behavior = None

    def reset(self) -> None:
        """Called whenever a behavioral transition (switch) occurs."""
        ...

    def is_active(self) -> bool:
        """Checks if the condition of the transition is true."""
        return False

    def __and__(self, other: Transition) -> Transition:
        """True when both are; `other` is checked only if `self` is true."""
        left, right = self, other

        class _And(Transition):
            def reset(self) -> None:
                left.reset()
                right.reset()

            def is_active(self) -> bool:
                return left.is_active() and right.is_active()

        return _And()

    def __invert__(self) -> Transition:
        """True when `self` is false."""
        inner = self

        class _Not(Transition):
            def reset(self) -> None:
                inner.reset()

            def is_active(self) -> bool:
                return not inner.is_active()

        return _Not()
