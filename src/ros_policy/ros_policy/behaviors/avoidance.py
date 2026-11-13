import math
import random

from ..state import State
from .behavior import Behavior


class Avoidance(Behavior):
    """Turns in place away from obstacles, in a direction picked once, so the robot does not oscillate."""

    def __init__(self, robot_state: State) -> None:
        self.state, self.turn = robot_state, 0

    def reset(self) -> None:
        left, right = sum(self.state.front[0, 1]), sum(self.state.front[3, 4])
        self.turn = (right > left) - (left > right) or random.choice((-1, 1))

    def step(self) -> None:
        self.state.set_heading(magnitude=1, angle=self.turn * math.pi)
