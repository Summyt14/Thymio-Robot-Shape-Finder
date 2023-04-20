from node import *


class Selector(Node):
    def __init__(self, node_list: list[Node]) -> None:
        super().__init__()
        self.node_list = node_list

    def evaluate(self) -> int:
        for node in self.node_list:
            evaluate_node = node.evaluate()
            if evaluate_node == RUNNING:
                self._node_state = RUNNING
                return self._node_state
            elif evaluate_node == SUCCESS:
                self._node_state = SUCCESS
                return self._node_state
            else:
                break

        self._node_state = FAILURE
        return self._node_state
