from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio
import time
import random


class Rotate(Node):
    """
    A class that handles the rotation of the thymio.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The first node.
        speed (int) : The speed of the motors.
        duration (int) : The time in seconds of rotation.
    """

    def __init__(self, th: Thymio, first_node: str, speed: int, duration: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.speed = speed
        self.duration = duration


    def evaluate(self) -> int:
        direction = random.randint(0,9)

        # 70% probability of turning to the right
        if direction > 2:
            self.th[self.first_node]["motor.left.target"] = self.speed
            self.th[self.first_node]["motor.right.target"] = -self.speed
        else:
            self.th[self.first_node]["motor.left.target"] = -self.speed
            self.th[self.first_node]["motor.right.target"] = self.speed

        time.sleep(self.duration)
        return SUCCESS

    def get_running_node(self) -> Node:
        return self
