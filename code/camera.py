import cv2
import threading
import pygame

DISCONNECTED = "Disconnected"
CONNECTED = "Connected"
CONNECTING = "Connecting"
ERROR = "Error"


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
        thread = threading.Thread(target=self.run_thread, args=(self.video_url,))
        thread.start()

    def apply_operators(self, frame):
        """
        Applies image processing operators to the given frame.

        Args:
            frame: The original video frame

        Returns:
            A tuple containing the original and processed frames.
        """
        # Grayscale, Otsu's threshold
        gray =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 9)
        _, threshold = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
  
        # list for storing names of shapes
        for contour in contours:
        
            # here we are ignoring first counter because 
            # findcontour function detects whole image as shape
            if i == 0:
                i = 1
                continue
            
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

            # using drawContours() function
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 5)

            x = y = 0
            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])

            # putting shape name at center of each shape
            if len(approx) == 3:
                cv2.putText(frame, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            elif len(approx) == 4:
                cv2.putText(frame, 'Quadrilateral', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            elif len(approx) == 5:
                cv2.putText(frame, 'Pentagon', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            elif len(approx) == 6:
                cv2.putText(frame, 'Hexagon', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            else:
                cv2.putText(threshold, 'circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        return frame, threshold

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

    def disconnect(self):
        """
        Disconnects from the IP camera.
        """
        self.status = DISCONNECTED
        if self.thread is not None:
            self.thread.join()
