from behavior_tree.base_nodes.base_node import *


class Idle(Node):
    """
    A class representing a node that is an idle state.
    """

    def __init__(self) -> None:
        super().__init__()

    def evaluate(self) -> int:
        return SUCCESS

    def get_running_node(self) -> Node:
        return self
