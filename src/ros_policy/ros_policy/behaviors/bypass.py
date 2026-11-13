import math
import random

from ..state import State
from .behavior import Behavior

PREY_DISTANCE = 0.096  # m, from the robot center to the center of a pushed prey (front tip 5.6 cm + prey radius 4 cm)
ORBIT_RADIUS = 0.14    # m, enough for the robot side (5.5 cm) to clear the prey (4 cm)


class Bypass(Behavior):
    """
    Drive around an object, towards the side of the darker ground sensor (the nest), then turns slowly back towards the
    prey.
    """

    def __init__(self, robot_state: State, period: float, angle: float, arc_speed: float) -> None:
        self.state = robot_state
        self.period = period
        self.angle = angle
        self.arc_speed = arc_speed
        self.side = 1  # +1: go around the prey keeping it on the left (counterclockwise), -1: on the right
        self.backoff_end = self.turn_end = self.arc_end = 0

    def reset(self) -> None:
        left, right = self.state.ground or (0.0, 0.0)
        self.side = (left < right) - (right < left) or random.choice((-1, 1))
        now = self.state.step_counter
        self.backoff_end = now + round((ORBIT_RADIUS - PREY_DISTANCE) / State.MAX_WHEEL_SPEED / self.period)
        self.turn_end = self.backoff_end + round(math.pi / 2 / State.ANGULAR_SPEED / self.period)
        self.arc_end = self.turn_end + round(self.angle * ORBIT_RADIUS / self.arc_speed / self.period)

    def step(self) -> None:
        now = self.state.step_counter
        if now < self.backoff_end:    # back off
            linear, angular = -State.MAX_WHEEL_SPEED, 0.0
        elif now < self.turn_end:     # turn sideways, away from the prey
            linear, angular = 0.0, -self.side * State.ANGULAR_SPEED
        elif now < self.arc_end:      # arc around the prey
            linear, angular = self.arc_speed, self.side * self.arc_speed / ORBIT_RADIUS
        else:                         # turn slowly back towards the prey
            linear, angular = 0.0, self.side * State.ANGULAR_SPEED / 2
        delta = angular * State.INTERWHEEL_DISTANCE / 2
        self.state.set_speed(*(max(-1.0, min(1.0, speed / State.MAX_WHEEL_SPEED)) for speed in (linear - delta, linear + delta)))
