from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class Backoff(Node):
    """
    A class representing a node makes the thymio back off to a certain distance.

    Args:
        th (Thymio): The Thymio robot.
        first_node (str): The first node.
        speed (int) : The speed of the motors
        back_distance (int): distance to where thymio backs off
    
    """

    def __init__(self, th: Thymio, first_node: str, speed: int, back_distance: int) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node
        self.speed = speed
        self.back_distance = back_distance

    def evaluate(self) -> int:
        sensors = self.th[self.first_node]["prox.horizontal"]
        self.th[self.first_node]["motor.left.target"] = -self.speed
        self.th[self.first_node]["motor.right.target"] = -self.speed

        if (sensors[5] == 0
            and sensors[6] == 0) :

            print("back cleared")
            print ("center ", sensors[2])

            if (0 < sensors[2] < self.back_distance):

                self.th[self.first_node]["motor.left.target"] = 0
                self.th[self.first_node]["motor.right.target"] = 0

                
                print("backed enough")

                return  SUCCESS

                


            return RUNNING
        
        return self._node_state
       

    def get_running_node(self) -> Node:
        return self
