import random
from typing import Optional

from dasher_assignment.models import Dasher
from dasher_assignment.pool import AvailableDashers


class RandomDasherPicker:
    """Offers each order to a uniformly random available dasher."""

    def __init__(self, pool: AvailableDashers, rng: Optional[random.Random] = None) -> None:
        self._pool = pool
        self._rng = rng or random.Random()

    def pick(self) -> Optional[Dasher]:
        if len(self._pool) == 0:
            return None
        return self._pool.at(self._rng.randrange(len(self._pool)))
