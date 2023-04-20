FAILURE = 0
RUNNING = 1
SUCCESS = 2


class Node:
    def __init__(self) -> None:
        self._node_state = SUCCESS

    def evaluate(self) -> int:
        pass
