import pygame
import math
from thymiodirect import Connection, Thymio


class ThymioController:
    def __init__(self) -> None:
        self.is_connected = False
        self.th = None
        self.node_id = None
        self.toggle_light = False

    def connect(self):
        try:
            port = Connection.serial_default_port()
            self.th = Thymio(serial_port=port, on_connect=lambda id: print(f"{id} is connected"))
            self.th.connect()
            self.node_id = self.th.first_node()
            self.is_connected = True
            return True
        except:
            return False

    def disconnect(self):
        # TODO i dont think this is the right function to disconnect
        if self.is_connected:
            self.th.disconnect()
            self.is_connected = False

    def handle_inputs(self, pressed_keys: dict):
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
        left_speed = int(speed * math.cos(angle))
        right_speed = int(speed * math.sin(angle))
        print("Left:", left_speed, "/ Right:", right_speed)

        if self.is_connected:
            self.th[self.node_id]["motor.left.target"] = left_speed
            self.th[self.node_id]["motor.right.target"] = right_speed
            self.th[self.node_id]["leds.top"] = [0, 0, 32] if self.toggle_light else [0, 0, 0]

    def run(self, pressed_keys: dict):
        self.handle_inputs(pressed_keys)
