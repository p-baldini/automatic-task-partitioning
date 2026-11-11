from .transition import Transition
from ..state import State


class Timed(Transition):
    """Active after a cooldown (in steps) has passed."""

    def __init__(self, robot: State, duration: int) -> None:
        self.now = lambda: robot.step_counter
        self.start = self.now()
        self.duration = duration

    def reset(self) -> None:
        self.start = self.now()

    def is_active(self) -> None:
        return self.now() - self.start > self.duration
