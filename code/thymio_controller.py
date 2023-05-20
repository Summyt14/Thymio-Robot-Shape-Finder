import pygame
import math
from camera import Camera
from behavior_tree.base_nodes import *
from behavior_tree.nodes import *
from thymiodirect import Connection, Thymio


TRIANGLE = "Triangle"
RECTANGLE = "Rectangle"
PENTAGON = "Pentagon"
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
        has_detected_correct_shape = HasDetectedCorrectShape(self)
        make_noise = MakeNoise(self.th, self.first_node)
        idle = Idle(self.th, self.first_node)
        shape_detect = Sequence([has_detected_correct_shape, make_noise, idle])


        rotate_robot = MoveRobotTime(self.th, self.first_node, 0, 100, 3)
        move_robot_away_obstacle = MoveRobotAwayObstacle(self.th, self.first_node, 100, 3500)
        avoid_object_seq = Sequence([move_robot_away_obstacle, rotate_robot])

        obstacle_detected = Inverter(ObstacleDetected(self.th, self.first_node, 2000))
        obstacle_handling = Selector([shape_detect, avoid_object_seq])


        # TODO this node
        move_forward = MoveForward(self.th, self.first_node, 50)
        has_object_front = Inverter(HasObjectInFront(self.th, self.first_node, 4500, 2000))
        move_sequence = Sequence([obstacle_detected, move_forward])
        
        
        align = Align(self.th, self.first_node, 15)
        backoff = Backoff(self.th, self.first_node, 50, 2500)
        idle_timer = IdleTimer(self.th, self.first_node, 2)
        align_sequence = Sequence([align, backoff, idle_timer])

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
            
        # self.handle_inputs(pressed_keys)
