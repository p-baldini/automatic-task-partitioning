from ..sensors import Sensors


class Behavior:
    """Represents a behavioral policy usable by the robot."""

    def reset(self, sensors: Sensors) -> None:
        """Called when the behavior becomes active."""
        ...

    def step(self, sensors: Sensors) -> None:
        """Execute the behavioral policy."""
        ...
