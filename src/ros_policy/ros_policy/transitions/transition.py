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
