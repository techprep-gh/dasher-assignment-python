from dataclasses import dataclass


@dataclass(frozen=True)
class Dasher:
    id: str
    name: str


@dataclass(frozen=True)
class Order:
    id: str
    store: str
    dropoff: str


@dataclass(frozen=True)
class Assignment:
    order_id: str
    dasher_id: str
    dispatch_node: str
