from behavior_tree.base_nodes.node import *
from thymio_controller import ThymioController


class HasObjectInFront(Node):
    """
    A class representing a node that checks if there is an object in front of the robot.

    The node checks the horizontal proximity sensors of the robot and returns SUCCESS if any of them
    detect an object within a certain distance. Otherwise, the node returns FAILURE.

    Args:
        controller (ThymioController): The controller for the Thymio robot.
        distance_check (int): The distance threshold to consider an obstacle.
    """
    def __init__(self, controller: ThymioController, distance_check: int) -> None:
        super().__init__()
        self.controller = controller
        self.th = controller.th
        self.node_id = controller.node_id
        self.distance_check = distance_check

    def evaluate(self) -> int:
        sensors = self.th[self.node_id]["prox.horizontal"]
        if sensors[0] > self.distance_check \
                or sensors[1] > self.distance_check \
                or sensors[2] > self.distance_check \
                or sensors[3] > self.distance_check \
                or sensors[4] > self.distance_check:
            self._node_state = SUCCESS
            return self._node_state

        self._node_state = FAILURE
        return self._node_state
