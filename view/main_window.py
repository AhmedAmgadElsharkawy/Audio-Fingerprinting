from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout

from view.input_viewer import InputViewer
from view.output_viewer import OutputViewer

from model.audio_signal_model import AudioSignalModel



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_signals = [AudioSignalModel(),AudioSignalModel()]
        self.output_signal = AudioSignalModel()

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.input_viewer = InputViewer(self.input_signals[0])
        self.main_layout.addWidget(self.input_viewer)

        self.output_viewer = OutputViewer(self.output_signal)
        self.main_layout.addWidget(self.output_viewer)
