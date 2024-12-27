from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout
from view.audio_viewer import AudioViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QHBoxLayout(self.main_widget)
        self.audio_viewer = AudioViewer()
        self.main_layout.addWidget(self.audio_viewer)
