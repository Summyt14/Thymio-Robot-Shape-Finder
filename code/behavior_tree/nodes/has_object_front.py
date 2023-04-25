from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class HasObjectInFront(Node):
    """
    A class representing a node that checks if there is an object in front of the robot.

    The node checks the horizontal proximity sensors of the robot and returns SUCCESS if any of them
    detect an object within a certain distance. Otherwise, the node returns FAILURE.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The main node id.
        distance_check (int): The distance threshold to consider an obstacle.
    """
    def __init__(self, th: Thymio, first_node: str, distance_check: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.distance_check = distance_check

    def evaluate(self) -> int:
        sensors = self.th[self.first_node]["prox.horizontal"]
        if sensors[0] > self.distance_check \
                or sensors[1] > self.distance_check \
                or sensors[2] > self.distance_check \
                or sensors[3] > self.distance_check \
                or sensors[4] > self.distance_check:
            self._node_state = SUCCESS
            return self._node_state

        self._node_state = FAILURE
        return self._node_state
    
    def get_running_node(self):
        return self
