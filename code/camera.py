import cv2
import threading
from queue import Queue

DISCONNECTED = "Disconnected"
CONNECTED = "Connected"
CONNECTING = "Connecting"
ERROR = "Error"


class Camera:
    def __init__(self) -> None:
        self.video_url = ""
        self.status = DISCONNECTED
        self.original_frame_queue = Queue()
        self.processed_frame_queue = Queue()
        self.thread = None
        self.lock = threading.Lock()

    def connect(self, ip: str):
        self.video_url = "http://%s:4747/video" % (ip)
        self.status = CONNECTING
        thread = threading.Thread(
            target=self.run_thread, args=(self.video_url,))
        thread.start()

    def apply_operators(self, frame):
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
                orignial_frame, processed_frame = self.apply_operators(frame)
                self.original_frame_queue.put(orignial_frame)
                self.processed_frame_queue.put(processed_frame)

    def run(self):
        if not self.original_frame_queue.empty() and not self.processed_frame_queue.empty():
            original_frame = self.original_frame_queue.get()
            processed_frame = self.processed_frame_queue.get()
            color_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
            gray_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            return color_frame, gray_frame
        else:
            return None, None

    def disconnect(self):
        self.status = DISCONNECTED
        if self.thread is not None:
            self.thread.join()
