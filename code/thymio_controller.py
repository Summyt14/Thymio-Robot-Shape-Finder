from camera import Camera
from behavior_tree.base_nodes import *
from behavior_tree.nodes import *
from thymiodirect import Connection, Thymio


TRIANGLE = "Triangle"
RECTANGLE = "Rectangle"
PENTAGON = "Pentagon"
HEXAGON = "Hexagon"
STAR = "Star"
CIRCLE = "Circle"


class ThymioController:
    """
    This class is the brain of the robot. It's responsible for translating the information it receives into physical behaviours.
    """
    def __init__(self, camera: Camera) -> None:
        self.camera = camera
        self.desired_shape = ""
        self.is_connected = False
        self.th = None
        self.first_node = None
        self.toggle_light = False
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        self.pressed_keys = dict()
        self.top_node = None
        self.avoiding_obstacle = False

    def construct_behavior_tree(self) -> None:
        """
        Constructs the behavior tree for the robot.
        """
        obstacle_detected = Inverter(HasDetectedObstacle(self.th, self.first_node, 2000))
        move_forward = MoveForward(self.th, self.first_node, 50)

        align = Align(self.th, self.first_node, 15)
        backoff = Backoff(self.th, self.first_node, 50, 2500)

        rotate = Rotate(self.th, self.first_node, 50, 4)

        has_detected_correct_shape = HasDetectedCorrectShape(self)
        flash_lights = FlashLights(self.th, self.first_node)
        idle = Idle(self.th, self.first_node)


        shape_detect = Sequence([has_detected_correct_shape, flash_lights, idle])
        obstacle_handling = Selector([shape_detect, rotate])
        align_sequence = Sequence([align, backoff, obstacle_handling])
        move_sequence = Sequence([obstacle_detected, move_forward])
        self.top_node = Selector([move_sequence, align_sequence])


    def connect(self) -> bool:
        """
        Connects to the Thymio robot via serial port.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            port = Connection.serial_default_port()
            self.th = Thymio(serial_port=port, 
                             on_connect=lambda name: print(f"{name} is connected"),
                             on_disconnect=lambda name: print(f"{name} is disconnected"),
                             on_comm_error=lambda name: print(f"{name} comm error"))
            self.th.connect()
            self.first_node = self.th.first_node()
            self.is_connected = True
            self.construct_behavior_tree()
            return True
        except:
            return False
        
    def set_desired_shape(self, button_index: int) -> None:
        """
        Sets the desired shape for the thymio to lookout for.
        
        Args:
            button_index (int): The index of the button pressed.
        """
        if button_index == 0:
            self.desired_shape = TRIANGLE
        elif button_index == 1:
            self.desired_shape = RECTANGLE
        elif button_index == 2:
            self.desired_shape = PENTAGON
        elif button_index == 3:
            self.desired_shape = HEXAGON
        elif button_index == 4:
            self.desired_shape = STAR
        elif button_index == 5:
            self.desired_shape = CIRCLE

    def disconnect(self) -> None:
        """
        Disconnects from the Thymio robot.
        """
        if self.is_connected:
            self.th[self.first_node]["motor.left.target"] = 0
            self.th[self.first_node]["motor.right.target"] = 0
            self.is_connected = False
            self.th.thymio_proxy.connection.shutdown()

    def run(self, pressed_keys: dict) -> None:
        self.pressed_keys = pressed_keys
        if self.is_connected:
            self.top_node.evaluate()
            