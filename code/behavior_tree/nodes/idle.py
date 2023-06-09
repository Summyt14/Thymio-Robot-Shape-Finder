from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class Idle(Node):
    """
    A class representing a node that is an idle state.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The first node.
    """

    def __init__(self, th: Thymio, first_node: str) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node

    def evaluate(self) -> int:
        self.th[self.first_node]["motor.left.target"] = 0
        self.th[self.first_node]["motor.right.target"] = 0
        return RUNNING

    def get_running_node(self) -> Node:
        return self
