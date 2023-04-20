from node import *


class Inverter(Node):
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