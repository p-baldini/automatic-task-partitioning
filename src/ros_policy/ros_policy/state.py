from dataclasses import dataclass
from typing import List


@dataclass
class State:
    """Latest known robot state."""
    step_counter: int               # a value containing the steps count since the start of the simulation.
    proximity: List[float] = None   # 7 values in [0,1]: the first 5 contain the value of the front proximity sensors,
                                    # left to right; the last 2 contains the value of the 2 rear sensors.
    ground: List[float] = None      # 2 values in [0,1]: left and right readings; empty until the first reading.
    motors: List[float] = None      # 2 values in [0,1]: left and right speeds.

    @property
    def front(self) -> List[float]:
        """Utility to access the front proximity readings."""
        return self.proximity[:5]

    @property
    def rear(self) -> List[float]:
        """Utility to access the rear proximity readings."""
        return self.proximity[-2:]

    @property
    def level(self) -> float:
        """Mean floor level under the ground sensors."""
        return sum(self.ground) / len(self.ground) if self.ground else 0.0
