import random

from dasher_assignment import AvailableDashers, RandomDasherPicker


def test_pick_returns_an_available_dasher(dasher):
    pool = AvailableDashers()
    for dasher_id in ("d1", "d2", "d3"):
        pool.add(dasher(dasher_id))
    picker = RandomDasherPicker(pool, random.Random(1))

    assert {picker.pick().id for _ in range(20)} <= {"d1", "d2", "d3"}


def test_pick_eventually_reaches_every_dasher(dasher):
    pool = AvailableDashers()
    for dasher_id in ("d1", "d2", "d3", "d4"):
        pool.add(dasher(dasher_id))
    picker = RandomDasherPicker(pool, random.Random(3))

    assert {picker.pick().id for _ in range(200)} == {"d1", "d2", "d3", "d4"}


def test_pick_never_returns_a_removed_dasher(dasher):
    pool = AvailableDashers()
    for dasher_id in ("d1", "d2", "d3"):
        pool.add(dasher(dasher_id))
    pool.remove("d1")
    picker = RandomDasherPicker(pool, random.Random(5))

    assert {picker.pick().id for _ in range(100)} == {"d2", "d3"}
