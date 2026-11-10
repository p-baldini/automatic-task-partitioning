from ..behaviors import Behavior
from ..sensors import Sensors


class Transition:
    """
    A condition that switches the FSM from the `origin` behavior to the `target` one (set by FSM.add_transition).
    An instance is one edge: to use the same condition on several edges, see Same.
    """
    origin: Behavior = None
    target: Behavior = None

    def reset(self, sensors: Sensors) -> None:
        """Called when the origin state becomes active."""
        ...

    def is_active(self, sensors: Sensors) -> bool:
        """Checks if the condition of the transition is true."""
        return False
