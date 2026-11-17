def is_wide(front: list, threshold: float) -> bool:
    """Whether the front sensors see something wider than a prey (a prey excites at most 3 adjacent central ones)."""
    active = [f > threshold for f in front]
    return sum(active) >= 4 or (sum(active) == 3 and (active[0] or active[4]))
