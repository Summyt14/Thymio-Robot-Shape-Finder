from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class HasDetectedObstacle(Node):
    """
    A class representing a node that is used to check if an obstacle is found at a certain distance.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The first node.
        distance_check (str) : The minimum distance to detect an obstacle.
    """

    def __init__(self, th: Thymio, first_node: str, distance_check: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.distance_check = distance_check

    def evaluate(self) -> int:
        sensors = self.th[self.first_node]["prox.horizontal"]
        if 0 < sensors[0] > self.distance_check \
                or 0 < sensors[1] > self.distance_check \
                or 0 < sensors[2] > self.distance_check \
                or 0 < sensors[3] > self.distance_check \
                or 0 < sensors[4] > self.distance_check:
            return SUCCESS
        else:
            return FAILURE

    def get_running_node(self) -> Node:
        return self
