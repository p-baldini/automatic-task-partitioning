from ..state import State
from .transition import Transition
from .wide import is_wide


class Prey(Transition):
    """Transition dependent on the presence (or lack) of a prey ahead."""

    def __init__(self, robot_state: State, threshold: float, negated: bool = False) -> None:
        self.state = robot_state
        self.threshold = threshold  # proximity in [0,1]
        self.negated = negated

    def is_active(self) -> bool:
        v = max(self.state.front) > self.threshold and not is_wide(self.state.front, self.threshold)
        return not v if self.negated else v
