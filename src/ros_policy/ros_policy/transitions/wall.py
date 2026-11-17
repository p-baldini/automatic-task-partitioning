from ..state import State
from .transition import Transition
from .wide import is_wide


class Wall(Transition):
    """Active when the front sensors see something wider than a prey for `steps` consecutive steps (a pushed prey
    looks wide too, but only for an instant while it slides across the front)."""

    def __init__(self, robot_state: State, threshold: float, steps: int) -> None:
        self.state, self.threshold, self.steps, self.count = robot_state, threshold, steps, 0

    def reset(self) -> None:
        self.count = 0

    def is_active(self) -> bool:
        self.count = self.count + 1 if is_wide(self.state.front, self.threshold) else 0
        return self.count >= self.steps
