import math

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class State:
    """Latest known robot state and information."""
    INTERWHEEL_DISTANCE = 0.08          # m, as in ros_thymio
    MAX_WHEEL_SPEED = 0.1               # m/s, ros_thymio's default max_wheel_speed (10 cm/s)
    ANGULAR_SPEED = 1.5                 # rad/s
    STEP_DURATION = 0.1                 # 100ms

    step_counter: int                   # a value containing the steps count since the start of the simulation.
    proximity: Tuple[7 * float] = None  # 7 values in [0,1]: the first 5 contain the value of the front proximity
                                        # sensors, left to right; the last 2 contains the value of the 2 rear sensors.
    ground: Tuple[2 * float] = None     # 2 values in [0,1]: left and right readings; empty until the first reading.
    motors: Tuple[2 * float] = None     # 2 values in [0,1]: left and right speeds.
    heading: Optional[Tuple[float, float]] = None  # (distance [m], angle [rad]) of the robot from the nest, the angle
                                                   # wrt the robot facing (positive left), at odometry_step; None if
                                                   # the nest is unknown. Kept up to date by odometry (see set_speed).
    odometry_step: int = 0                         # step at which the heading was last updated.

    def set_nest(self) -> None:
        """The robot is at the nest now: from here on, odometry tracks the heading (see nest)."""
        self.heading, self.odometry_step = (0.0, 0.0), self.step_counter

    @property
    def nest(self) -> Optional[Tuple[float, float]]:
        """The heading now: (distance [m], angle [rad]) of the robot from the nest; none if the nest is unknown."""
        return odometry(self)

    @property
    def front(self) -> Tuple[float]:
        """Utility to access the front proximity readings."""
        return self.proximity[:5]

    @property
    def rear(self) -> Tuple[float]:
        """Utility to access the rear proximity readings."""
        return self.proximity[-2:]

    @property
    def level(self) -> float:
        """Mean floor level under the ground sensors."""
        return sum(self.ground) / len(self.ground) if self.ground else 0.0

    def set_heading(self, magnitude: float, angle: float) -> None:
        """Convert magnitude and direction to left and right wheel speeds and set them to the robot."""
        angle = math.atan2(math.sin(angle), math.cos(angle))  # normalize to [-pi, pi]
        linear, angular = magnitude * max(0.0, math.cos(angle)), angle * self.INTERWHEEL_DISTANCE / 2
        self.set_speed(linear - angular, linear + angular)

    def set_speed(self, left_velocity: float, right_velocity: float) -> None:
        """Set left and right wheel speeds of the motors (in [-1,1]). Update the nest position accordingly."""
        self.heading, self.odometry_step = odometry(self), self.step_counter
        self.motors = [round(left_velocity, 2), round(right_velocity, 2)]


def odometry(state: State) -> Optional[Tuple[float, float]]:
    """The heading now, given the motors kept their speeds since odometry_step."""
    dt = (state.step_counter - state.odometry_step) * state.STEP_DURATION
    if state.heading is None or dt <= 0 or not state.motors:
        return state.heading
    left, right = (m * state.MAX_WHEEL_SPEED for m in state.motors)
    linear, angular = (left + right) / 2, (right - left) / state.INTERWHEEL_DISTANCE
    turn = angular * dt
    # Constant speeds drive an arc: its chord points halfway through the turn
    chord = linear * dt if abs(turn) < 1e-9 else 2 * linear / angular * math.sin(turn / 2)
    # Add the step to the heading, then turn the heading by the robot turn (the angle is wrt the robot facing)
    distance, angle = state.heading
    x = distance * math.cos(angle) + chord * math.cos(turn / 2)
    y = distance * math.sin(angle) + chord * math.sin(turn / 2)
    angle = math.atan2(y, x) - turn
    return math.hypot(x, y), math.atan2(math.sin(angle), math.cos(angle))
