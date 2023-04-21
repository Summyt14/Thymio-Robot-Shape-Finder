from behavior_tree.base_nodes.node import *
from thymio_controller import ThymioController


class MoveRobotAwayObstacle(Node):
    """
    A class representing a node that moves the robot away from an obstacle.

    Args:
        controller (ThymioController): The controller for the Thymio robot.
        speed (int): The speed at which to move the robot.
        distance_check (int): The distance threshold to consider an obstacle.
        obstacle_in_front (bool, optional): Whether to move the robot away from an obstacle in front or behind it.
            Defaults to True.
    """
    def __init__(self, controller: ThymioController, speed: int, distance_check: int, obstacle_in_front: bool = True) -> None:
        super().__init__()
        self.controller = controller
        self.th = controller.th
        self.node_id = controller.node_id
        self.speed = speed
        self.distance_check = distance_check
        self.obstacle_in_front = obstacle_in_front

    def evaluate(self) -> int:
        sensors = self.th[self.node_id]["prox.horizontal"]
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
            
        self.th[self.node_id]["motor.left.target"] = final_speed
        self.th[self.node_id]["motor.right.target"] = final_speed
        return self._node_state
