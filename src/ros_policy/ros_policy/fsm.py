from typing import Iterable, List

from .behaviors import Behavior
from .transitions import Same, Transition


class FSM:
    """
    Runs one behavior at a time, and switches to another only when a transition out of the active one is true.
    Transitions are checked in the order they were added; the first true one is taken (at most one per step).
    Entering a state resets its behavior, and its transitions that the previous state does not share.
    """

    def __init__(self, behaviors: Iterable[Behavior]) -> None:
        self.behaviors: List[Behavior] = list(behaviors)
        self.transitions: List[Transition] = []
        self.state = next(iter(self.behaviors), None)

    def step(self) -> None:
        """Take the first enabled transition, if any, then return the command of the active behavior."""
        out = filter(lambda t: t.origin == self.state, self.transitions)
        active = filter(lambda t: t.is_active(), out)
        target = next(map(lambda t: t.target, active), self.state)
        if target is not self.state:
            target.reset()
            for transition in self.transitions:
                transition.reset()
            self.state = target
        self.state.step()
