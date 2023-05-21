from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class AvoidFall(Node):
    """
    A class representing a node that avoids the thymio from falling.
    """

    def __init__(self, th: Thymio, first_node: str, distance: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.distance = distance

    def evaluate(self) -> int:
        sensors = self.th[self.first_node]["prox.ground.reflected"]

        if sensors[0] < self.distance or 0 < sensors[1] < self.distance:
            self.th[self.first_node]["motor.left.target"] = 0
            self.th[self.first_node]["motor.right.target"] = 0
            
            return SUCCESS
        
        else:
            return FAILURE

    def get_running_node(self) -> Node:
        return self
