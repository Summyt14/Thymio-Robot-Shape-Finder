from behavior_tree.base_nodes.base_node import *


class HasDetectedCorrectShape(Node):
    """
    A class that represents a node that asks the camera for detected shapes and checks if its the one choosen by the user.

    Args:
        controller (ThymioController): The controller of the thymio.
    """

    def __init__(self, controller: any) -> None:
        super().__init__()
        self.controller = controller

    def evaluate(self) -> int:
        if self.controller.camera.status == "Connected":
            self.controller.camera.status = "Detecting"

        if self.controller.camera.status in ["Finished", "Debug"]:
            print(f"Selected: {self.controller.desired_shape}, Detected: {self.controller.camera.detected_shapes}")
            if len(self.controller.camera.detected_shapes) == 0:
                return FAILURE
            if self.controller.desired_shape in self.controller.camera.detected_shapes:
                return SUCCESS
            else:
                return FAILURE

        return RUNNING

    def get_running_node(self) -> Node:
        return self
