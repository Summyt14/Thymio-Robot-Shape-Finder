from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio
import time


class IdleTimer(Node):
    """
    A class representing a node that is an idle state.
    """

    def __init__(self, th: Thymio, first_node: str, duration: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.duration = duration

    def evaluate(self) -> int:

        print("waiting")

        self.th[self.first_node]["motor.left.target"] = 0
        self.th[self.first_node]["motor.right.target"] = 0
        
        time.sleep(self.duration)
        

        self._node_state = SUCCESS

        return self._node_state


    def get_running_node(self) -> Node:
        return self
