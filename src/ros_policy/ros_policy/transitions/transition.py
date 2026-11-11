from ..behaviors import Behavior
from ..sensors import Sensors


class Transition:
    """A condition to enable the passage from one behavior to another."""
    origin: Behavior = None
    target: Behavior = None

    def reset(self, sensors: Sensors) -> None:
        """Called when the origin state becomes active."""
        ...

    def is_active(self, sensors: Sensors) -> bool:
        """Checks if the condition of the transition is true."""
        return False
