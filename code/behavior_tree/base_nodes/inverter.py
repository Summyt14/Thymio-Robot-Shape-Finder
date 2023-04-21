from node import *


class Inverter(Node):
    """
    A class representing an inverter node in a behavior tree.

    The inverter node inverts the result of its child node. If the child node returns FAILURE,
    the inverter node returns SUCCESS. If the child node returns SUCCESS, the inverter node
    returns FAILURE. If the child node returns RUNNING, the inverter node also returns RUNNING.

    Args:
        node (Node): The child node to invert.
    """
    def __init__(self, node: Node) -> None:
        super().__init__()
        self.node = node

    def evaluate(self) -> int:
        evaluate_node = self.node.evaluate()
        
        if evaluate_node == RUNNING:
            self._node_state = RUNNING
        elif evaluate_node == SUCCESS:
            self._node_state = FAILURE
        else:
            self._node_state = SUCCESS

        return self._node_state