import pytest

from dasher_assignment import RoundRobinRouter
from dasher_assignment.errors import DispatchNodeAlreadyRegistered, UnknownDispatchNode


def route_many(router, order, count):
    return [router.route(order(f"o{i}")) for i in range(count)]


def test_nodes_take_turns_in_order(order):
    router = RoundRobinRouter(["dispatch-1", "dispatch-2", "dispatch-3"])

    assert route_many(router, order, 6) == [
        "dispatch-1",
        "dispatch-2",
        "dispatch-3",
        "dispatch-1",
        "dispatch-2",
        "dispatch-3",
    ]


def test_a_node_marked_up_again_rejoins_the_rotation(order):
    router = RoundRobinRouter(["dispatch-1", "dispatch-2", "dispatch-3"])
    router.mark_down("dispatch-2")
    router.mark_up("dispatch-2")

    assert route_many(router, order, 3) == ["dispatch-1", "dispatch-2", "dispatch-3"]
    assert router.healthy_nodes() == ["dispatch-1", "dispatch-2", "dispatch-3"]


def test_healthy_nodes_excludes_nodes_marked_down():
    router = RoundRobinRouter(["dispatch-1", "dispatch-2", "dispatch-3"])
    router.mark_down("dispatch-3")

    assert router.healthy_nodes() == ["dispatch-1", "dispatch-2"]


def test_unknown_node_cannot_be_marked():
    router = RoundRobinRouter(["dispatch-1"])

    with pytest.raises(UnknownDispatchNode):
        router.mark_down("dispatch-9")


def test_added_node_joins_the_end_of_the_rotation(order):
    router = RoundRobinRouter(["dispatch-1", "dispatch-2"])
    router.add_node("dispatch-3")

    assert route_many(router, order, 4) == ["dispatch-1", "dispatch-2", "dispatch-3", "dispatch-1"]
    assert router.healthy_nodes() == ["dispatch-1", "dispatch-2", "dispatch-3"]


def test_node_added_at_runtime_and_marked_down_is_skipped(order):
    router = RoundRobinRouter(["dispatch-1", "dispatch-2"])
    router.add_node("dispatch-3")
    router.mark_down("dispatch-3")

    assert route_many(router, order, 4) == ["dispatch-1", "dispatch-2", "dispatch-1", "dispatch-2"]


def test_adding_a_known_node_is_rejected():
    router = RoundRobinRouter(["dispatch-1"])

    with pytest.raises(DispatchNodeAlreadyRegistered):
        router.add_node("dispatch-1")
