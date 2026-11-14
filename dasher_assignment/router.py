from typing import Iterable, List

from dasher_assignment.availability import AVAILABLE, UNAVAILABLE, NodeAvailability
from dasher_assignment.errors import DispatchNodeAlreadyRegistered, NoHealthyDispatchNode
from dasher_assignment.models import Order


class RoundRobinRouter:
    """Spreads offers across dispatch nodes in turn, skipping nodes that are unavailable."""

    def __init__(self, nodes: Iterable[str]) -> None:
        self._nodes: List[str] = list(nodes)
        self._availability = NodeAvailability(self._nodes)
        self._cursor = 0

    def add_node(self, node: str) -> None:
        if node in self._nodes:
            raise DispatchNodeAlreadyRegistered(node)
        self._nodes.append(node)
        self._availability.register(node)

    def set_availability(self, node: str, state: str) -> None:
        self._availability.set_state(node, state)

    def mark_down(self, node: str) -> None:
        self.set_availability(node, UNAVAILABLE)

    def mark_up(self, node: str) -> None:
        self.set_availability(node, AVAILABLE)

    def healthy_nodes(self) -> List[str]:
        return [node for node in self._nodes if self._availability.is_available(node)]

    def route(self, order: Order) -> str:
        """Pick the dispatch node for this order. Round robin does not look at the order."""
        for _ in range(len(self._nodes)):
            node = self._nodes[self._cursor]
            self._cursor = (self._cursor + 1) % len(self._nodes)
            if self._availability.is_available(node):
                return node
        raise NoHealthyDispatchNode()
