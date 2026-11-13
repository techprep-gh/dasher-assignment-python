import random

import pytest

from dasher_assignment import AssignmentService, Dasher, Order, RoundRobinRouter


# pytest-timeout cannot see debugpy (its trace function has no module), so a paused
# breakpoint would be killed after the timeout.
def pytest_configure(config):
    import sys

    if sys.gettrace() is not None and config.pluginmanager.has_plugin("pytest_timeout"):
        config.pluginmanager.unregister(name="pytest_timeout")


@pytest.fixture
def make_service():
    def make(nodes=("dispatch-1", "dispatch-2"), seed=7):
        return AssignmentService(RoundRobinRouter(nodes), rng=random.Random(seed))

    return make


@pytest.fixture
def dasher():
    def make(dasher_id):
        return Dasher(id=dasher_id, name=f"Dasher {dasher_id}")

    return make


@pytest.fixture
def order():
    def make(order_id):
        return Order(id=order_id, store="Golden Wok", dropoff="12 Mission St")

    return make
