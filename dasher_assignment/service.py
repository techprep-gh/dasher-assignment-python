import random
from typing import Dict, List, Optional

from dasher_assignment.errors import UnknownOrder
from dasher_assignment.models import Assignment, Dasher, Order
from dasher_assignment.picker import RandomDasherPicker
from dasher_assignment.pool import AvailableDashers
from dasher_assignment.router import RoundRobinRouter


class AssignmentService:
    def __init__(self, router: RoundRobinRouter, rng: Optional[random.Random] = None) -> None:
        self._router = router
        self._pool = AvailableDashers()
        self._picker = RandomDasherPicker(self._pool, rng)
        self._active: Dict[str, Assignment] = {}
        self._dashers: Dict[str, Dasher] = {}

    def go_online(self, dasher: Dasher) -> None:
        self._pool.add(dasher)
        self._dashers[dasher.id] = dasher

    def go_offline(self, dasher_id: str) -> None:
        self._pool.remove(dasher_id)

    def is_online(self, dasher_id: str) -> bool:
        return dasher_id in self._pool

    def available_dashers(self) -> List[str]:
        return self._pool.ids()

    def assign(self, order: Order) -> Optional[Assignment]:
        """Offer the order to a random available dasher, or return None if nobody is free."""
        dasher = self._picker.pick()
        if dasher is None:
            return None
        node = self._router.next_node()
        self._pool.remove(dasher.id)
        assignment = Assignment(order_id=order.id, dasher_id=dasher.id, dispatch_node=node)
        self._active[order.id] = assignment
        return assignment

    def active_assignment(self, order_id: str) -> Optional[Assignment]:
        return self._active.get(order_id)

    def complete(self, order_id: str) -> None:
        """Close the delivery and put the dasher back in the pool for the next order."""
        assignment = self._active.pop(order_id, None)
        if assignment is None:
            raise UnknownOrder(order_id)
        self._pool.add(self._dashers[assignment.dasher_id])
