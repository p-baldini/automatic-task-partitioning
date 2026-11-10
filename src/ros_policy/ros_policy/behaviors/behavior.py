from ..sensors import Sensors


class Behavior:
    """Drives the robot while it is the active state of the FSM (see fsm.py)."""

    def reset(self, sensors: Sensors) -> None:
        """Called when the behavior becomes active."""
        ...

    def step(self, sensors: Sensors) -> tuple:
        """Return the (linear [m/s], angular [rad/s]) command."""
        raise NotImplementedError
