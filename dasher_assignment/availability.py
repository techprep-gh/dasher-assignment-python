from typing import Dict, Iterable

from dasher_assignment.errors import InvalidAvailabilityState, UnknownDispatchNode

AVAILABLE = "AVAILABLE"
UNAVAILABLE = "UNAVAILABLE"
STATES = (AVAILABLE, UNAVAILABLE)


class NodeAvailability:
    """Availability state per dispatch node, as reported by health checks."""

    def __init__(self, nodes: Iterable[str]) -> None:
        self._states: Dict[str, str] = {node: AVAILABLE for node in nodes}

    def register(self, node: str) -> None:
        self._states[node] = AVAILABLE

    def set_state(self, node: str, state: str) -> None:
        if node not in self._states:
            raise UnknownDispatchNode(node)
        if state not in STATES:
            raise InvalidAvailabilityState(state)
        self._states[node] = state

    def is_available(self, node: str) -> bool:
        return self._states[node] == AVAILABLE
