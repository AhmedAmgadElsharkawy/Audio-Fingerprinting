from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout
from view.input_viewer import InputViewer

from model.audio_signal_model import AudioSignalModel



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_signals = [AudioSignalModel(),AudioSignalModel()]

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.audio_viewer = InputViewer(self.input_signals[0])
        self.main_layout.addWidget(self.audio_viewer)
