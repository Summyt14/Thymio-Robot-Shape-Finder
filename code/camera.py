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
        thread = threading.Thread(target=self.run_thread, args=(self.video_url,))
        thread.start()

    def apply_operators(self, frame):
        # Grayscale, Otsu's threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        return thresh

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
                self.original_frame_queue.put(frame)
                self.processed_frame_queue.put(self.apply_operators(frame))

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
