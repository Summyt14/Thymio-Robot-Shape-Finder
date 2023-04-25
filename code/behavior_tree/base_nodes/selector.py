from .base_node import *


class Selector(Node):
    """
    A class representing a selector node in a behavior tree.

    The selector node executes its child nodes in order until one of them returns either SUCCESS or
    RUNNING. If a child node returns RUNNING, the selector node returns RUNNING and will continue
    to execute the next child node on the next evaluation. If a child node returns SUCCESS, the
    selector node returns SUCCESS and will not execute any further child nodes. If all child nodes
    return FAILURE, the selector node returns FAILURE.

    Args:
        node_list (list[Node]): The list of child nodes to execute.
    """
    def __init__(self, node_list: list[Node]) -> None:
        super().__init__()
        self.node_list = node_list

    def evaluate(self) -> int:
        for node in self.node_list:
            evaluate_node = node.evaluate()
            if evaluate_node == RUNNING:
                self._node_state = RUNNING
                self._running_node = node.get_running_node()
                return self._node_state
            elif evaluate_node == SUCCESS:
                self._node_state = SUCCESS
                return self._node_state
            else:
                break

        self._node_state = FAILURE
        return self._node_state

    def get_running_node(self) -> Node:
        return self._running_node