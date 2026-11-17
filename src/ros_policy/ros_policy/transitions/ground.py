from typing import Tuple

from ..state import State
from .transition import Transition

Range = Tuple[float, float]  # [low, high) floor levels


class Ground(Transition):
    """Active when the mean floor level is in the `threshold` range [low, high)."""

    def __init__(self, robot_state: State, threshold: Range) -> None:
        self.state = robot_state
        self.threshold = threshold

    def is_active(self) -> bool:
        return bool(self.state.ground) and self.threshold[0] <= self.state.level < self.threshold[1]
