from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class HasObjectInFront(Node):
    """
    A class representing a node that checks if there is an object in front of the robot.

    The node checks the horizontal proximity sensors of the robot and returns SUCCESS if any of them
    detect an object within a certain distance. Otherwise, the node returns FAILURE.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The main node id.
        fst_distance_check (int): The first distance threshold to consider an obstacle.
        snd_distance_check (int): The second distance threshold to consider an obstacle.
    """
    def __init__(self, th: Thymio, first_node: str, fst_distance_check: int, snd_distance_check: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.fst_distance_check = fst_distance_check
        self.snd_distance_check = snd_distance_check
        self.avoiding_obstacle = False

    def evaluate(self) -> int:
        sensors = self.th[self.first_node]["prox.horizontal"]
        print(sensors)
        if (sensors[0] > self.snd_distance_check) \
                or (sensors[1] > self.snd_distance_check) \
                or (sensors[2] > self.snd_distance_check) \
                or (sensors[3] > self.snd_distance_check) \
                or (sensors[4] > self.snd_distance_check):
            if (self.avoiding_obstacle):
                self._node_state = SUCCESS
                return self._node_state
            
            if (sensors[0] > self.fst_distance_check) \
                    or (sensors[1] > self.fst_distance_check) \
                    or (sensors[2] > self.fst_distance_check) \
                    or (sensors[3] > self.fst_distance_check) \
                    or (sensors[4] > self.fst_distance_check):
               self.avoiding_obstacle = True
            else:
                self._node_state = FAILURE
                return self._node_state
        else:
            self.avoiding_obstacle = False
            self._node_state = FAILURE
            return self._node_state
        
    def get_running_node(self):
        return self
