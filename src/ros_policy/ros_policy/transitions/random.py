from random import Random

from .transition import Transition


class Random(Transition):
    """A transition that becomes active with a fixed probability."""

    def __init__(self, probability: float = 0.5) -> None:
        self.random = Random() # TODO use seed or a singleton rng
        self.probability = probability

    def is_active(self) -> bool:
        return self.random() < self.probability
