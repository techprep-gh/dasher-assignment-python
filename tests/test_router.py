import pytest

from dasher_assignment import RoundRobinRouter
from dasher_assignment.errors import UnknownDispatchNode


def test_nodes_take_turns_in_order():
    router = RoundRobinRouter(["dispatch-1", "dispatch-2", "dispatch-3"])

    assert [router.next_node() for _ in range(6)] == [
        "dispatch-1",
        "dispatch-2",
        "dispatch-3",
        "dispatch-1",
        "dispatch-2",
        "dispatch-3",
    ]


def test_a_node_marked_up_again_rejoins_the_rotation():
    router = RoundRobinRouter(["dispatch-1", "dispatch-2", "dispatch-3"])
    router.mark_down("dispatch-2")
    router.mark_up("dispatch-2")

    assert [router.next_node() for _ in range(3)] == ["dispatch-1", "dispatch-2", "dispatch-3"]
    assert router.healthy_nodes() == ["dispatch-1", "dispatch-2", "dispatch-3"]


def test_healthy_nodes_excludes_nodes_marked_down():
    router = RoundRobinRouter(["dispatch-1", "dispatch-2", "dispatch-3"])
    router.mark_down("dispatch-3")

    assert router.healthy_nodes() == ["dispatch-1", "dispatch-2"]


def test_unknown_node_cannot_be_marked():
    router = RoundRobinRouter(["dispatch-1"])

    with pytest.raises(UnknownDispatchNode):
        router.mark_down("dispatch-9")
