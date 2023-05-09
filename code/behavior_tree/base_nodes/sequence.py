from .base_node import *


class Sequence(Node):
    """
    A class representing a sequence node in a behavior tree.

    The sequence node executes its child nodes in order until one of them returns either FAILURE or
    RUNNING. If a child node returns RUNNING, the sequence node returns RUNNING and will continue
    to execute the next child node on the next evaluation. If a child node returns FAILURE, the
    sequence node returns FAILURE and will not execute any further child nodes. If all child nodes
    return SUCCESS, the sequence node returns SUCCESS.

    Args:
        node_list (list[Node]): The list of child nodes to execute.
    """

    def __init__(self, node_list: list[Node]) -> None:
        super().__init__()
        self.node_list = node_list

    def evaluate(self) -> int:
        is_any_node_running = False

        for node in self.node_list:
            evaluate_node = node.evaluate()
            if evaluate_node == RUNNING:
                is_any_node_running = True
                self._running_node = node.get_running_node()
                break
            elif evaluate_node == SUCCESS:
                continue
            else:
                self._node_state = FAILURE
                return self._node_state

        self._node_state = RUNNING if is_any_node_running else SUCCESS
        return self._node_state

    def get_running_node(self) -> Node:
        return self._running_node
