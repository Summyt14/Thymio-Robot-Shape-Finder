from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class Align(Node):
    """
    A class representing a node that handles the alignment with an obstacle.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The first node.
        speed (int) : The speed of the motors.
    """

    def __init__(self, th: Thymio, first_node: str, speed: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.speed = speed

    def evaluate(self) -> int:
        sensors = self.th[self.first_node]["prox.horizontal"]
        calibrate_delay = 850

        # Turn the robot slightly to the left
        if sensors[1] > sensors[3] + calibrate_delay:
            self.th[self.first_node]["motor.left.target"] = -self.speed
            self.th[self.first_node]["motor.right.target"] = self.speed
            self._node_state = RUNNING
        
        # Turn the robot slightly to the right
        elif sensors[3] > sensors[1] + calibrate_delay:
            self.th[self.first_node]["motor.left.target"] = self.speed
            self.th[self.first_node]["motor.right.target"] = -self.speed
            self._node_state = RUNNING
        else:
            self._node_state = SUCCESS

        return self._node_state

    def get_running_node(self) -> Node:
        return self
