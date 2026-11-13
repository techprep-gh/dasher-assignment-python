class AssignmentError(Exception):
    pass


class DasherAlreadyOnline(AssignmentError):
    def __init__(self, dasher_id: str):
        super().__init__(f"dasher {dasher_id} is already online")
        self.dasher_id = dasher_id


class UnknownDasher(AssignmentError):
    def __init__(self, dasher_id: str):
        super().__init__(f"dasher {dasher_id} is not online")
        self.dasher_id = dasher_id


class UnknownOrder(AssignmentError):
    def __init__(self, order_id: str):
        super().__init__(f"order {order_id} has no active assignment")
        self.order_id = order_id


class UnknownDispatchNode(AssignmentError):
    def __init__(self, node: str):
        super().__init__(f"dispatch node {node} is not registered")
        self.node = node


class NoHealthyDispatchNode(AssignmentError):
    def __init__(self):
        super().__init__("no healthy dispatch node")
