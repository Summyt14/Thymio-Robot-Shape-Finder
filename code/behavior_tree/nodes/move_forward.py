from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class MoveForward(Node):
    """
    A class representing the exploration of thymio.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The first node.
        speed (int) : The speed of the motors
    """

    def __init__(self, th: Thymio, first_node: str, speed: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.speed = speed

    def evaluate(self) -> int:
        self.th[self.first_node]["motor.left.target"] = self.speed
        self.th[self.first_node]["motor.right.target"] = self.speed
        return RUNNING

    def get_running_node(self) -> Node:
        return self
