import math
import random
from collections import deque

from ..state import State
from .behavior import Behavior


class Thigmotaxis(Behavior):
    """
    Klinotaxis on the floor gradient, too shallow to be sensed across the two ground sensors: goes straight while the
    floor got lighter (climb) or darker (descend) by `threshold` over the last `window` steps, turns otherwise.
    """

    def __init__(self, robot_state: State, window: int, threshold: float, climb: bool = True) -> None:
        self.state = robot_state
        self.threshold, self.sign = threshold, 1.0 if climb else -1.0
        self.history, self.turn = deque(maxlen=window + 1), 0

    def reset(self) -> None:
        self.history.clear()
        self.turn = 0

    def step(self) -> None:
        self.history.append(self.state.level)
        progress = self.sign * (self.history[-1] - self.history[0])
        if progress > self.threshold:
            self.turn = 0
        elif progress < -self.threshold and not self.turn:
            self.turn = random.choice((-1, 1))
        self.state.set_heading(magnitude=1, angle=self.turn * math.pi)
