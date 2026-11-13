from ..state import State
from .behavior import Behavior


class Transport(Behavior):
    """Pushes the prey ahead straight, steering to keep it centered."""

    def __init__(self, robot_state: State, push_speed: float = 0.5, centering_gain: float = 1) -> None:
        self.state, self.push_speed, self.centering_gain = robot_state, push_speed, centering_gain

    def step(self) -> None:
        front = self.state.front
        self.state.set_heading(self.push_speed, self.centering_gain * (front[0] + front[1] - front[3] - front[4]))
