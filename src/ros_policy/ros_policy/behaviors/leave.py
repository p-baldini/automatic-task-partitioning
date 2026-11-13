import math
import random

from ..state import State
from .behavior import Behavior


class Leave(Behavior):
    """Backs off, turns in place by a random angle, then stops."""

    def __init__(self, robot_state: State, period: float, backoff_time: float, linear_speed: float,
                 angular_speed: float, min_angle: float = math.pi / 2) -> None:
        self.state, self.period = robot_state, period
        self.backoff_time, self.min_angle, self.angular_speed = backoff_time, min_angle, angular_speed
        self.backoff = linear_speed / State.MAX_WHEEL_SPEED                                      # wheel speed
        self.spin = angular_speed * State.INTERWHEEL_DISTANCE / 2 / State.MAX_WHEEL_SPEED        # wheel speed
        self.turn = 0  # +1: turn left (counterclockwise), -1: turn right
        self.backoff_end = self.turn_end = 0

    def reset(self) -> None:
        left, right = self.state.front[0] + self.state.front[1], self.state.front[3] + self.state.front[4]
        self.turn = (right > left) - (left > right) or random.choice((-1, 1))
        angle = random.uniform(self.min_angle, math.pi)
        self.backoff_end = self.state.step_counter + round(self.backoff_time / self.period)
        self.turn_end = self.backoff_end + round(angle / self.angular_speed / self.period)

    def step(self) -> None:
        now = self.state.step_counter
        if now < self.backoff_end:
            self.state.set_speed(-self.backoff, -self.backoff)
        elif now < self.turn_end:
            self.state.set_speed(-self.turn * self.spin, self.turn * self.spin)
        else:
            self.state.set_speed(0.0, 0.0)
