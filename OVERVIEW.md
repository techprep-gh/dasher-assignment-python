# Dasher assignment overview

The in-process core of a delivery service's dasher assignment. When an order is
ready for pickup, the service offers it to a random dasher who is online and
free, and sends the offer through one of the dispatch nodes, which take turns.

## Terms

- **Dasher:** a courier. A dasher is online when they are free to take an order.
  While delivering, they are out of the pool until the delivery is completed.
- **Pool:** the dashers who are online and free right now.
- **Dispatch node:** a backend that sends offers to dashers' phones. Health
  checks report each node's availability, and nodes that are down are skipped.
- **Assignment:** an order matched to a dasher and a dispatch node.

## Lifecycle

1. `go_online(dasher)` puts a dasher in the pool.
2. `assign(order)` picks a dasher, routes the offer to a dispatch node and takes
   the dasher out of the pool while they deliver.
3. `complete(order_id)` closes the delivery and puts the dasher back in the pool.
4. `go_offline(dasher_id)` takes a free dasher out of the pool.

## Modules

All in `dasher_assignment/`:

- `service.py`: `AssignmentService`, the lifecycle above
- `pool.py`: `AvailableDashers`, the pool
- `picker.py`: `RandomDasherPicker`, picks a dasher from the pool
- `router.py`: `RoundRobinRouter`, chooses the dispatch node for each offer
- `availability.py`: `NodeAvailability`, each dispatch node's availability state
- `models.py`: `Dasher`, `Order` and `Assignment`, the records the service passes around
- `errors.py`: the service's exceptions

## Running the tests

```bash
pytest tests/
```
