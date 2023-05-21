from behavior_tree.base_nodes.base_node import *
from thymiodirect import Thymio
import time


class FlashLights(Node):
    """
    A class that flashes the lights. 
    """

    def __init__(self, th: Thymio, first_node: str) -> None:
        super().__init__()
        self.th = th
        self.first_node = first_node

    def evaluate(self) -> int:
        self.th[self.first_node]["leds.top"] = [0, 255, 0]
        time.sleep(0.5)
        self.th[self.first_node]["leds.top"] = [0, 0, 0]
        time.sleep(0.5)
        self.th[self.first_node]["leds.top"] = [0, 0, 255]
        time.sleep(0.5)
        self.th[self.first_node]["leds.top"] = [0, 0, 0]
        return RUNNING

    def get_running_node(self) -> Node:
        return self

