from typing import Dict, List

from dasher_assignment.errors import DasherAlreadyOnline, UnknownDasher
from dasher_assignment.models import Dasher


class AvailableDashers:
    """Dashers waiting for an offer, with O(1) add, remove and access by position."""

    def __init__(self) -> None:
        self._dashers: List[Dasher] = []
        self._positions: Dict[str, int] = {}

    def __len__(self) -> int:
        return len(self._dashers)

    def __contains__(self, dasher_id: object) -> bool:
        return dasher_id in self._positions

    def add(self, dasher: Dasher) -> None:
        if dasher.id in self._positions:
            raise DasherAlreadyOnline(dasher.id)
        self._positions[dasher.id] = len(self._dashers)
        self._dashers.append(dasher)

    def remove(self, dasher_id: str) -> Dasher:
        if dasher_id not in self._positions:
            raise UnknownDasher(dasher_id)
        position = self._positions.pop(dasher_id)
        removed = self._dashers[position]
        last = self._dashers.pop()
        if position < len(self._dashers):
            self._dashers[position] = last
            self._positions[last.id] = position
        return removed

    def at(self, position: int) -> Dasher:
        return self._dashers[position]

    def ids(self) -> List[str]:
        return [dasher.id for dasher in self._dashers]
