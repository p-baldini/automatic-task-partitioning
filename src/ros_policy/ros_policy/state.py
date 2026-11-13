import math

from dataclasses import dataclass
from typing import Tuple


@dataclass
class State:
    """Latest known robot state and information."""
    INTERWHEEL_DISTANCE = 0.08          # m, as in ros_thymio
    MAX_WHEEL_SPEED = 0.1               # m/s, ros_thymio's default max_wheel_speed (10 cm/s)

    step_counter: int                   # a value containing the steps count since the start of the simulation.
    proximity: Tuple[7 * float] = None  # 7 values in [0,1]: the first 5 contain the value of the front proximity
                                        # sensors, left to right; the last 2 contains the value of the 2 rear sensors.
    ground: Tuple[2 * float] = None     # 2 values in [0,1]: left and right readings; empty until the first reading.
    motors: Tuple[2 * float] = None     # 2 values in [0,1]: left and right speeds.

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
        """Set left and right wheel speeds of the motors."""
        self.motors = [round(left_velocity, 2), round(right_velocity, 2)]
