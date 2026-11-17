"""A FSMs generator and mutator."""
import copy
import itertools
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


def _link(t: Transition, origin: Behavior, target: Behavior) -> Transition:
    """Set the origin and target of the transition, and return it."""
    t.origin, t.target = origin, target
    return t


def random_fsm(robot: State, max_behaviors: int, max_transitions: int, rng: random.Random = random) -> FSM:
    """
    An FSM with 1 to `max_behaviors` random behaviors, each with 0 to `max_transitions` random transitions
    to another behavior. The first behavior is the initial state.
    """
    behaviors = [_behavior(robot, rng) for _ in range(rng.randint(1, max_behaviors))]

    def out_of(origin: Behavior) -> list[Transition]:
        targets = [b for b in behaviors if b is not origin]
        count = rng.randint(0, max_transitions) if targets else 0
        return [_link(_transition(robot, rng), origin, rng.choice(targets)) for _ in range(count)]

    transitions = [t for origin in behaviors for t in out_of(origin)]

    return FSM(behaviors, transitions)


def mutate(fsm: FSM, robot: State, max_behaviors: int, max_transitions: int, p: float,
           rng: random.Random = random) -> FSM:
    """A changed copy of `fsm` (left untouched). With probability `p` each: a behavior is removed (with its
    transitions in and out) or substituted, equally likely; a transition's condition is substituted, else it is removed; and, repeatedly
    while under the limits, a behavior is added, a transition is added out of each behavior."""
    child = copy.deepcopy(fsm, {id(robot): robot})  # the copy reads the same robot state

    # decide whether to keep a behavior or change it; if decided to change, the possibilities are remove or substitute
    fate = lambda b: b if rng.random() > p else rng.choice([None, _behavior(robot, rng)])

    # change the behavior set, ensuring that at least a behavior exists
    new = { b: fate(b) for b in child.behaviors }  # old behavior -> new one, or None if removed
    kept = [b for b in new.values() if b] or [_behavior(robot, rng)]

    # consider adding a behavior to the set
    added = itertools.takewhile(lambda _: rng.random() < p, range(max_behaviors - len(kept)))
    behaviors = kept + [_behavior(robot, rng) for _ in added]

    # drop the transitions of removed behaviors, and remove each of the others with probability p
    survivors = [t for t in child.transitions if new.get(t.origin) and new.get(t.target) and rng.random() >= p]

    # substitute the condition with probability p, and attach to the new origin and target
    kept_t = [
        _link(_transition(robot, rng) if rng.random() < p else t, new[t.origin], new[t.target])
        for t in survivors
    ]

    # consider adding transitions out of each behavior, while under the limit
    def additions(origin: Behavior) -> list:
        targets = [b for b in behaviors if b is not origin]
        free = max_transitions - sum(t.origin is origin for t in kept_t) if targets else 0
        added = itertools.takewhile(lambda _: rng.random() < p, range(free))
        return [_link(_transition(robot, rng), origin, rng.choice(targets)) for _ in added]

    transitions = kept_t + [t for origin in behaviors for t in additions(origin)]

    return FSM(behaviors, transitions)
