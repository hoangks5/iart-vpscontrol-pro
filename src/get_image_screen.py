import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QRubberBand
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QRect, QSize
from PIL import ImageGrab
from PyQt6.QtCore import pyqtSignal
from PIL import Image
import io
import base64
import time




class ScreenCapture(QMainWindow):
    finished = pyqtSignal(str)  # Emit Base64 string instead of no args

    def __init__(self, parent=None):
        super().__init__()
        self.ui = parent
        self.screenshot = self.capture_screen()
        self.pixmap = QPixmap.fromImage(self.pil_image_to_qimage(self.screenshot))

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.setWindowTitle("Select a region")

        self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.origin = None

        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.setCentralWidget(self.label)

        self.setFixedSize(screen.size())

        self.setMouseTracking(True)
        self.label.setMouseTracking(True)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

    def capture_screen(self):
        screenshot = ImageGrab.grab()
        return screenshot

    def pil_image_to_qimage(self, pil_image):
        rgb_image = pil_image.convert("RGB")
        qimage = QImage(rgb_image.tobytes(), rgb_image.width, rgb_image.height, rgb_image.width * 3, QImage.Format.Format_RGB888)
        return qimage

    def image_to_base64(self, image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return base64_string

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.origin = event.position().toPoint()
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.origin is not None:
            rect = QRect(self.origin, event.position().toPoint()).normalized()
            self.rubberBand.setGeometry(rect)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.origin is not None:
            rect = QRect(self.origin, event.position().toPoint()).normalized()
            x, y, width, height = rect.getRect()

            # Capture the selected region from the screenshot
            selected_image = self.screenshot.crop((x, y, x + width, y + height))
            
            # Convert the image to Base64
            base64_string = self.image_to_base64(selected_image)
            
            if self.ui:
                # You can also use clipboard if needed
                clipboard = QApplication.clipboard()
                clipboard.setText(base64_string)
                time.sleep(0.2)
            # Emit the Base64 string
            self.finished.emit(base64_string)
            self.close()