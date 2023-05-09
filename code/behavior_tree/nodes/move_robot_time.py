from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio
import time


class MoveRobotTime(Node):
    """
    A class representing a node that moves the Thymio robot for a certain duration of time.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The first node.
        left_speed (int): The speed of the left motor.
        right_speed (int): The speed of the right motor.
        duration (float): The duration in seconds to move the robot.
    """
    def __init__(self, th: Thymio, first_node: str, left_speed: int, right_speed: int, duration: float) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.left_speed = left_speed
        self.right_speed = right_speed
        self.duration = duration
        self.start_time = None

    def evaluate(self) -> int:
        if self.start_time is None:
            self.start_time = time.time()
        
        elapsed_time = time.time() - self.start_time
        remaining_time = max(self.duration - elapsed_time, 0)
        
        if remaining_time > 0:
            self.th[self.first_node]["motor.left.target"] = self.left_speed
            self.th[self.first_node]["motor.right.target"] = self.right_speed
            self._node_state = RUNNING
            print("im turning")
        else:
            self.th[self.first_node]["motor.left.target"] = 0
            self.th[self.first_node]["motor.right.target"] = 0
            self._node_state = SUCCESS
            print("i stopped turning")

        return self._node_state
    
    def get_running_node(self) -> Node:
        return self
