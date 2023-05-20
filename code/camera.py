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
    """
    def __init__(self) -> None:
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

        if self.status not in [DETECTING, DEBUG]:
            return frame, thresh

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.detected_shapes.clear()

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 1000 or area > 150000:
                continue

            cv2.drawContours(frame, [contour], -1, (255, 0, 0), 5)
            x = y = 0
            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])

            # find number of edges
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            edges = len(approx)
            shape_name = self.get_shape_name(edges)
            self.detected_shapes.append(shape_name)

            # Create a separate image for the text
            text_img = np.zeros_like(frame)
            cv2.putText(text_img, shape_name, (y, x), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            # Mirror the text image horizontally
            mirrored_text_img = cv2.flip(text_img, 1)
            # Rotate the text by 90 degrees
            rows, cols, _ = mirrored_text_img.shape
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
            rotated_text_img = cv2.warpAffine(mirrored_text_img, M, (cols, rows))

            # Overlay the rotated text onto the original image
            frame = cv2.add(frame, rotated_text_img)

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

    def get_shape_name(self, edges: int) -> str:
        """
        Returns the name of a shape given the number of edges.

        Args:
            edges (int): The number of edges.
        Returns:
            str: The name of the shape.
        """
        if edges == 3:
            return "Triangle"
        elif edges == 4:
            return "Rectangle"
        elif edges == 5:
            return "Pentagon"
        else:
            return "Circle"

    def disconnect(self):
        """
        Disconnects from the IP camera.
        """
        self.status = DISCONNECTED
        if self.thread is not None:
            self.thread.join()
