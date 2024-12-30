from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageDisplay:
    @staticmethod
    def load_and_scale_image(image_path, width, height):
        try:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                return pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
        return None

    @staticmethod
    def update_label_with_image(label: QLabel, image_path: str, width: int, height: int):
        scaled_pixmap = ImageDisplay.load_and_scale_image(image_path, width, height)
        if scaled_pixmap:
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignCenter)