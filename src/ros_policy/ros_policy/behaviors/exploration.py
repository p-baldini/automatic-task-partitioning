import math
import random

from ..state import State
from .behavior import Behavior


# TODO move it to a proper place
MAX_TURN = math.ceil(2 * math.pi / (ANGULAR_SPEED := 1.5) / 0.1)    # 2π / 1.5 ≈ 4.19 s -> 4.19 / 0.1 ≈ 42 steps for a
                                                                    # full turn, where 0.1 is the step duration.


class Exploration(Behavior):
    """Random walk: straight runs and turns in place, both of random duration (in steps)."""

    def __init__(self, robot_state: State, max_straight: int) -> None:
        self.state = robot_state
        self.max_straight = max_straight
        self.duration = 0

    def reset(self) -> None:
        self.state.set_heading(magnitude=1, angle=0)
        self.duration = random.randint(0, self.max_straight)

    def step(self) -> None:
        if self.duration <= 0:
            if self.state.motors[0] == self.state.motors[1]:
                self.state.set_heading(magnitude=1, angle=random.choice((-math.pi, math.pi)))
                self.duration = random.randint(0, MAX_TURN)
            else:
                self.reset()
        self.duration = self.duration - 1
