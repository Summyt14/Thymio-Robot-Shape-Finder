from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio


class MakeNoise(Node):
    """
    A class representing 
    """

    def __init__(self, th: Thymio, first_node: str) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node

    def evaluate(self) -> int:
        # self.th noise ....
        return SUCCESS

    def get_running_node(self) -> Node:
        return self

