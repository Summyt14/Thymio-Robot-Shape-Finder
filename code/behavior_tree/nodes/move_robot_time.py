from behavior_tree.base_nodes.node import *
from thymio_controller import ThymioController
import time


class MoveRobotTime(Node):
    """
    A class representing a node that moves the Thymio robot for a certain duration of time.

    Args:
        controller (ThymioController): The controller for the Thymio robot.
        left_speed (int): The speed of the left motor.
        right_speed (int): The speed of the right motor.
        duration (float): The duration in seconds to move the robot.
    """
    def __init__(self, controller: ThymioController, left_speed: int, right_speed: int, duration: float) -> None:
        super().__init__()
        self.controller = controller
        self.th = controller.th
        self.node_id = controller.node_id
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
            self.th[self.node_id]["motor.left.target"] = self.left_speed
            self.th[self.node_id]["motor.right.target"] = self.right_speed
            self._node_state = RUNNING
        else:
            self.th[self.node_id]["motor.left.target"] = 0
            self.th[self.node_id]["motor.right.target"] = 0
            self._node_state = SUCCESS

        return self._node_state
