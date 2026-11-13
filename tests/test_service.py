import pytest

from dasher_assignment.errors import UnknownDasher, UnknownOrder


def test_assign_offers_the_order_to_an_online_dasher(make_service, dasher, order):
    service = make_service()
    service.go_online(dasher("d1"))
    service.go_online(dasher("d2"))

    assignment = service.assign(order("o1"))

    assert assignment.order_id == "o1"
    assert assignment.dasher_id in {"d1", "d2"}
    assert assignment.dispatch_node == "dispatch-1"
    assert service.active_assignment("o1") == assignment


def test_orders_are_spread_across_dispatch_nodes(make_service, dasher, order):
    service = make_service()
    for dasher_id in ("d1", "d2", "d3"):
        service.go_online(dasher(dasher_id))

    nodes = [service.assign(order(f"o{i}")).dispatch_node for i in range(3)]

    assert nodes == ["dispatch-1", "dispatch-2", "dispatch-1"]


def test_each_order_goes_to_a_different_dasher(make_service, dasher, order):
    service = make_service()
    for dasher_id in ("d1", "d2", "d3"):
        service.go_online(dasher(dasher_id))

    dashers = {service.assign(order(f"o{i}")).dasher_id for i in range(3)}

    assert dashers == {"d1", "d2", "d3"}


def test_completing_an_unknown_order_raises(make_service):
    service = make_service()

    with pytest.raises(UnknownOrder):
        service.complete("o404")


def test_going_offline_twice_raises(make_service, dasher):
    service = make_service()
    service.go_online(dasher("d1"))
    service.go_online(dasher("d2"))
    service.go_offline("d1")

    with pytest.raises(UnknownDasher):
        service.go_offline("d1")
