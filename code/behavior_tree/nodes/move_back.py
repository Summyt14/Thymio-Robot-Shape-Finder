from behavior_tree.base_nodes.node import *
from thymiodirect import Thymio


class MoveBack(Node):
    def __init__(self, th: Thymio, node_id) -> None:
        super().__init__()
        self.th = th
        self.node_id = node_id

    def evaluate(self) -> int:
        self.th[self.node_id]["motor.left.target"] = -100
        self.th[self.node_id]["motor.right.target"] = -100
        self._node_state = RUNNING
        return self._node_state
