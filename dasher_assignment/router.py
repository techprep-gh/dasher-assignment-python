from typing import Iterable, List

from dasher_assignment.errors import (
    DispatchNodeAlreadyRegistered,
    NoHealthyDispatchNode,
    UnknownDispatchNode,
)
from dasher_assignment.models import Order


class RoundRobinRouter:
    """Spreads offers across dispatch nodes in turn, skipping nodes marked down."""

    def __init__(self, nodes: Iterable[str]) -> None:
        self._nodes: List[str] = list(nodes)
        self._healthy = set(self._nodes)
        self._cursor = 0

    def add_node(self, node: str) -> None:
        if node in self._nodes:
            raise DispatchNodeAlreadyRegistered(node)
        self._nodes.append(node)
        self._healthy.add(node)

    def mark_down(self, node: str) -> None:
        self._check_known(node)
        self._healthy.discard(node)

    def mark_up(self, node: str) -> None:
        self._check_known(node)
        self._healthy.add(node)

    def healthy_nodes(self) -> List[str]:
        return [node for node in self._nodes if node in self._healthy]

    def route(self, order: Order) -> str:
        """Pick the dispatch node for this order. Round robin does not look at the order."""
        for _ in range(len(self._nodes)):
            node = self._nodes[self._cursor]
            self._cursor = (self._cursor + 1) % len(self._nodes)
            if node in self._healthy:
                return node
        raise NoHealthyDispatchNode()

    def _check_known(self, node: str) -> None:
        if node not in self._nodes:
            raise UnknownDispatchNode(node)
