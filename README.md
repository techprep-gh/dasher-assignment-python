# Dasher assignment

The in-process core of the dasher assignment service. When an order is ready for
pickup, the service offers it to a random dasher who is online and free, and hands
the offer to one of the dispatch nodes, which take turns.

## Modules

- `dasher_assignment/pool.py`: `AvailableDashers`, the dashers waiting for an offer.
  A list plus an id-to-position map, so adding, removing and reading by position are O(1).
- `dasher_assignment/picker.py`: `RandomDasherPicker`, a uniform random pick from the pool.
- `dasher_assignment/router.py`: `RoundRobinRouter`, which routes each order to the
  dispatch nodes in turn, skipping any node marked down by health checks. Nodes can be
  added while the service runs.
- `dasher_assignment/service.py`: `AssignmentService`, which dashers go online and
  offline through, and which assigns and completes orders.

## Lifecycle

1. `go_online(dasher)` puts a dasher in the pool.
2. `assign(order)` picks a dasher, routes the offer to a dispatch node and takes the
   dasher out of the pool while they deliver. It returns `None` when nobody is free.
3. `complete(order_id)` closes the delivery and puts the dasher back in the pool.
4. `go_offline(dasher_id)` takes a free dasher out of the pool.

```python
from dasher_assignment import AssignmentService, Dasher, Order, RoundRobinRouter

service = AssignmentService(RoundRobinRouter(["dispatch-1", "dispatch-2"]))
service.go_online(Dasher(id="d1", name="Ana"))
assignment = service.assign(Order(id="o1", store="Golden Wok", dropoff="12 Mission St"))
service.complete(assignment.order_id)
```

## Tests

```bash
pip install -r requirements.txt
pytest
```
