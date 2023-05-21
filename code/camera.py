import cv2
import threading
import pygame
import numpy as np

DISCONNECTED = "Disconnected"
CONNECTED = "Connected"
CONNECTING = "Connecting"
DETECTING = "Detecting"
FINISHED = "Finished"
ERROR = "Error"
DEBUG = "Debug"


class Camera:
    """
    Camera class for connecting to an IP camera and processing its frames.

    Attributes:
        DISCONNECTED (str): A string constant representing the disconnected status.
        CONNECTED (str): A string constant representing the connected status.
        CONNECTING (str): A string constant representing the connecting status.
        ERROR (str): A string constant representing the error status.
    
    Args:
        is_debug (bool): Start camera in debug mode.
    """
    def __init__(self, is_debug: bool = False) -> None:
        self.is_debug = is_debug
        self.video_url = ""
        self.status = DISCONNECTED
        self.original_frame = None
        self.processed_frame = None
        self.detected_shapes = []
        self.thread = None
        self.lock = threading.Lock()

    def connect(self, ip: str):
        """
        Connects to a camera via IP address and starts a new thread to handle the frames.

        Args:
            ip (str): The IP address of the camera
        """
        self.video_url = "http://%s:4747/video" % (ip)
        self.status = CONNECTING
        self.thread = threading.Thread(target=self.run_thread, args=(self.video_url,))
        self.thread.start()

    def apply_operators(self, frame):
        """
        Applies image processing operators to the given frame.

        Args:
            frame: The original video frame

        Returns:
            A tuple containing the original and processed frames.
        """
        gray =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        thresh = (255 - thresh)

        if self.status not in [DETECTING, DEBUG]:
            return frame, thresh

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.detected_shapes.clear()

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 4000 or area > 30000:
                continue

            shape_name = self.get_shape_name(contour)
            self.detected_shapes.append(shape_name)

            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 5)

        if self.status != DEBUG:
            self.status = FINISHED
        return frame, thresh

    def run_thread(self, video_url: str):
        """
        Runs the thread for capturing and processing frames from the IP camera.

        Args:
            video_url (str): The URL of the video stream from the camera.
        """
        cap = cv2.VideoCapture(video_url)
        if not cap.isOpened():
            self.status = ERROR
            return

        self.status = CONNECTED
        if self.is_debug:
            self.status = DEBUG
        while True:
            ret, frame = cap.read()
            if not ret or self.status == DISCONNECTED or self.status == ERROR:
                self.status = ERROR
                break
            with self.lock:
                # Crop the top 15 pixels to remove watermark from the video
                frame = frame[15:, :]
                frame = cv2.flip(frame, 0)
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                original_frame, processed_frame = self.apply_operators(frame)
                original_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
                processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                self.original_frame = pygame.surfarray.make_surface(original_frame)
                self.processed_frame = pygame.surfarray.make_surface(processed_frame)

    def get_shape_name(self, contour) -> str:
        """
        Returns the name of a shape given the number of edges.

        Args:
            edges (int): The number of edges.
        Returns:
            str: The name of the shape.
        """
        # find number of edges
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        edges = len(approx)

        if edges == 3:
            return "Triangle"
        elif edges == 4:
            return "Rectangle"
        elif edges == 5:
            return "Pentagon"
        elif edges == 6:
            return "Hexagon"
        elif edges == 10:
            return "Star"
        else:
            return "Circle"

    def disconnect(self):
        """
        Disconnects from the IP camera.
        """
        self.status = DISCONNECTED
        if self.thread is not None:
            self.thread.join()
