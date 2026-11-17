from ..state import State
from .transition import Transition


class Obstacle(Transition):
    """Active when the front sensors see anything."""

    def __init__(self, robot_state: State, threshold: float) -> None:
        self.state, self.threshold = robot_state, threshold

    def is_active(self) -> bool:
        return max(self.state.front) > self.threshold
