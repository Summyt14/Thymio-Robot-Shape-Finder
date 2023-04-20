from behavior_tree.base_nodes.node import *
from thymiodirect import Thymio


class HasObjectInFront(Node):
    def __init__(self, th: Thymio, node_id) -> None:
        super().__init__()
        self.th = th
        self.node_id = node_id

    def evaluate(self) -> int:
        sensors = self.th[self.node_id]["prox.horizontal"]
        if sensors[0] > 4000 or sensors[5] > 4000:
            self._node_state = SUCCESS
            return self._node_state
        
        self._node_state = FAILURE
        return self._node_state