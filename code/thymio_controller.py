import pygame
import math
from behavior_tree.base_nodes import *
from behavior_tree.nodes import *
from thymiodirect import Connection, Thymio


class ThymioController:
    """
    This class is the brain of the robot. It's responsible for translating the information it receives into physical behaviours.
    """
    def __init__(self) -> None:
        self.is_connected = False
        self.th = None
        self.first_node = None
        self.toggle_light = False
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        self.pressed_keys = dict()
        self.top_node = None

    def construct_behavior_tree(self) -> None:
        """
        Constructs the behavior tree for the robot.
        """
        has_object_front = HasObjectInFront(self.th, self.first_node, 4000)
        move_robot_away_obstacle = MoveRobotAwayObstacle(self.th, self.first_node, 250, 2000)
        rotate_robot = MoveRobotTime(self.th, self.first_node, 100, 200, 1)
        avoid_object_seq = Sequence(list(has_object_front, move_robot_away_obstacle, rotate_robot))
        idle = Idle()

        self.top_node = Selector(list(avoid_object_seq, idle))

    def connect(self) -> bool:
        """
        Connects to the Thymio robot via serial port.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            port = Connection.serial_default_port()
            self.th = Thymio(serial_port=port, on_connect=lambda name: print(f"{name} is connected"))
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
        # TODO i dont think this is the right function to disconnect
        if self.is_connected:
            self.th.disconnect()
            self.is_connected = False

    # TODO this function needs to be convert into a node class 
    def handle_inputs(self, pressed_keys: dict) -> None:
        """
        Handles input from the keyboard and converts it into movement commands for the Thymio robot.

        Args: 
            pressed_keys (dict): A dictionary containing the keys that are currently pressed on the keyboard
        """
        forward_input = turn_input = 0
        for key in pressed_keys.keys():
            if key == pygame.K_w:
                forward_input = 1
            elif key == pygame.K_s:
                forward_input = -1
            elif key == pygame.K_a:
                turn_input = -1
            elif key == pygame.K_d:
                turn_input = 1
            elif key == pygame.K_SPACE:
                self.toggle_light = not self.toggle_light
        
        angle = math.atan2(turn_input, forward_input)
        speed = int(math.sqrt(forward_input**2 + turn_input**2) * 500)
        self.left_motor_speed = int(speed * math.cos(angle))
        self.right_motor_speed = int(speed * math.sin(angle))

        if self.is_connected:
            self.th[self.first_node]["motor.left.target"] = self.left_motor_speed
            self.th[self.first_node]["motor.right.target"] = self.right_motor_speed
            self.th[self.first_node]["leds.top"] = [0, 0, 32] if self.toggle_light else [0, 0, 0]

    def run(self, pressed_keys: dict) -> None:
        self.pressed_keys = pressed_keys
        if self.is_connected:
            self.top_node.evaluate()
            
        # self.handle_inputs(pressed_keys)
