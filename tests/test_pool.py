import pytest

from dasher_assignment import AvailableDashers
from dasher_assignment.errors import DasherAlreadyOnline, UnknownDasher


def test_added_dashers_are_available(dasher):
    pool = AvailableDashers()
    pool.add(dasher("d1"))
    pool.add(dasher("d2"))

    assert len(pool) == 2
    assert "d1" in pool and "d2" in pool
    assert pool.ids() == ["d1", "d2"]


def test_adding_the_same_dasher_twice_is_rejected(dasher):
    pool = AvailableDashers()
    pool.add(dasher("d1"))

    with pytest.raises(DasherAlreadyOnline):
        pool.add(dasher("d1"))


def test_removing_a_dasher_moves_the_last_one_into_its_slot(dasher):
    pool = AvailableDashers()
    for dasher_id in ("d1", "d2", "d3", "d4"):
        pool.add(dasher(dasher_id))

    removed = pool.remove("d2")

    assert removed.id == "d2"
    assert pool.ids() == ["d1", "d4", "d3"]
    assert "d2" not in pool
    assert [pool.at(i).id for i in range(len(pool))] == ["d1", "d4", "d3"]


def test_removed_dasher_can_be_added_again(dasher):
    pool = AvailableDashers()
    pool.add(dasher("d1"))
    pool.add(dasher("d2"))

    pool.remove("d1")
    pool.add(dasher("d1"))

    assert sorted(pool.ids()) == ["d1", "d2"]


def test_removing_an_unknown_dasher_raises(dasher):
    pool = AvailableDashers()
    pool.add(dasher("d1"))

    with pytest.raises(UnknownDasher):
        pool.remove("d9")
