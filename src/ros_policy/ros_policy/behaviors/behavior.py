class Behavior:
    """Represents a behavioral policy usable by the robot."""

    def reset(self) -> None:
        """Called when the behavior becomes active."""
        ...

    def step(self) -> None:
        """Execute the behavioral policy."""
        ...
