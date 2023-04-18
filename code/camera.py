import cv2


class Camera:
    def __init__(self, url: str) -> None:
        self.url = url
        self.cap = cv2.VideoCapture(self.url)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 15

    def apply_operators(self, frame):
        # Grayscale, Otsu's threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        return thresh

    def run(self):
        ret, frame = self.cap.read()
        # Crop the top 15 pixels to remove watermark from the video
        frame = frame[15:, :]
        frame = cv2.flip(frame, 0)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        after_frame = self.apply_operators(frame)
        return frame, after_frame

    def disconnect(self):
        self.cap.release()
