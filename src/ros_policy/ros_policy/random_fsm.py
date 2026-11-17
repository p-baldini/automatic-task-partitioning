"""A FSMs generator and mutator."""
import copy
import math
import random

from .behaviors import Avoidance, Behavior, Bypass, Exploration, Leave, Thigmotaxis, Transport
from .fsm import FSM
from .state import State, Zone
from .transitions import Ground, Obstacle, Prey, Timed, Transition, Wall

# Same defaults as the node in __main__.py
PERIOD = 0.1  # s, control period
THRESHOLD = 0.1
steps = lambda seconds: max(1, round(seconds / PERIOD))


def _behavior(r: State, rng: random.Random) -> Behavior:
    return rng.choice([
        lambda: Exploration(r, steps(5.0)),
        lambda: Thigmotaxis(r, steps(1.5), climb=rng.random() < 0.5),
        lambda: Avoidance(r),
        lambda: Transport(r),
        lambda: Bypass(r, PERIOD, math.radians(75.0), 0.08),
        lambda: Leave(r, PERIOD, 1.0, 0.08, 1.5),
    ])()


def _transition(r: State, rng: random.Random) -> Transition:
    return rng.choice([
        lambda: Prey(r, THRESHOLD),
        lambda: ~Prey(r, THRESHOLD),
        lambda: Obstacle(r, THRESHOLD),
        lambda: ~Obstacle(r, THRESHOLD),
        lambda: Wall(r, THRESHOLD, 3),
        lambda: ~Wall(r, THRESHOLD, 3),
        lambda: Ground(r, rng.choice(list(Zone)).value),
        lambda: ~Ground(r, rng.choice(list(Zone)).value),
        lambda: Timed(r, steps(3.0)),
    ])()


def random_fsm(robot: State, max_behaviors: int, max_transitions: int, rng: random.Random = random) -> FSM:
    """
    An FSM with 1 to `max_behaviors` random behaviors, each with 0 to `max_transitions` random transitions
    to another behavior. The first behavior is the initial state.
    """
    fsm = FSM(_behavior(robot, rng) for _ in range(rng.randint(1, max_behaviors)))
    for origin in fsm.behaviors:
        targets = [b for b in fsm.behaviors if b is not origin]
        for _ in range(rng.randint(0, max_transitions) if targets else 0):
            transition = _transition(robot, rng)
            transition.origin, transition.target = origin, rng.choice(targets)
            fsm.transitions.append(transition)
    return fsm
