FAILURE = 0
RUNNING = 1
SUCCESS = 2


class Node:
    """
    An abstract class for building behavior trees.

    Attributes:
        FAILURE (int): The node state for a failed node.
        RUNNING (int): The node state for a node that is still running.
        SUCCESS (int): The node state for a successful node.
    """
    def __init__(self) -> None:
        self._node_state = SUCCESS
        self._running_node = None

    def evaluate(self) -> int:
        """
        Evaluates the node and returns its state.

        Returns:
            int: The state of the node, either FAILURE, RUNNING, or SUCCESS.
        """
        pass

    def get_running_node(self):
        """
        Get the current running node.

        Returns:
            Node: The current running node.
        """
        return self._running_node
