from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class MoveRobotAwayObstacle(Node):
    """
    A class representing a node that moves the robot away from an obstacle.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The first node.
        speed (int): The speed at which to move the robot.
        distance_check (int): The distance threshold to consider an obstacle.
        obstacle_in_front (bool, optional): Whether to move the robot away from an obstacle in front or behind it.
            Defaults to True.
    """
    def __init__(self, th: Thymio, first_node: str, speed: int, distance_check: int, obstacle_in_front: bool = True) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.speed = speed
        self.distance_check = distance_check
        self.obstacle_in_front = obstacle_in_front

    def evaluate(self) -> int:
        sensors = self.th[self.first_node]["prox.horizontal"]
        final_speed = 0

        if self.obstacle_in_front:
            if 0 < sensors[0] > self.distance_check \
                    and 0 < sensors[1] > self.distance_check \
                    and 0 < sensors[2] > self.distance_check \
                    and 0 < sensors[3] > self.distance_check \
                    and 0 < sensors[4] > self.distance_check:
                final_speed = 0
                self._node_state = SUCCESS
            else:
                final_speed = -self.speed
                self._node_state = RUNNING
        else:
            if 0 < sensors[5] > self.distance_check \
                    and 0 < sensors[6] > self.distance_check:
                final_speed = 0
                self._node_state = SUCCESS
            else:
                final_speed = self.speed
                self._node_state = RUNNING
            
        self.th[self.first_node]["motor.left.target"] = final_speed
        self.th[self.first_node]["motor.right.target"] = final_speed
        return self._node_state
    
    def get_running_node(self) -> Node:
        return self
