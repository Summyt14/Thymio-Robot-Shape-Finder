from node import *


class Sequence(Node):
    def __init__(self, node_list: list[Node]) -> None:
        super().__init__()
        self.node_list = node_list

    def evaluate(self) -> int:
        is_any_node_running = False

        for node in self.node_list:
            evaluate_node = node.evaluate()
            if evaluate_node == RUNNING:
                is_any_node_running = True
                break
            elif evaluate_node == SUCCESS:
                break
            else:
                self._node_state = FAILURE
                return self._node_state

        self._node_state = RUNNING if is_any_node_running else SUCCESS
        return self._node_state