from behavior_tree.base_nodes.base_node import *


class HasDetectedCorrectShape(Node):
    """
    A class representing 
    """

    def __init__(self, controller: any) -> None:
        super().__init__()
        self.controller = controller

    def evaluate(self) -> int:
        if self.controller.camera.status == "Connected":
            self.controller.camera.status = "Detecting"
            if self.controller.camera.detected_shapes[0] == self.controller.desired_shape:
                # maybe wait a few secs for camera -> return RUNNING
                return SUCCESS
            else:
                return FAILURE

        return FAILURE

    def get_running_node(self) -> Node:
        return self
