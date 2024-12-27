from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout

from view.input_viewer import InputViewer
from view.output_viewer import OutputViewer

from model.audio_signal_model import AudioSignalModel

from view.list_viewer import ListViewer



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.input_signals = [AudioSignalModel(),AudioSignalModel()]
        self.output_signal = AudioSignalModel()

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QHBoxLayout(self.main_widget)

        self.viewers_widget = QWidget()
        self.viewers_widget_layout = QVBoxLayout(self.viewers_widget)
        
        self.main_widget_layout.addWidget(self.viewers_widget)
        
        self.input_viewers_widget = QWidget()
        self.input_viewers_widget_layout = QHBoxLayout(self.input_viewers_widget)
        self.viewers_widget_layout.addWidget(self.input_viewers_widget)


        self.input_viewer1 = InputViewer(self.input_signals[0])
        self.input_viewer2 = InputViewer(self.input_signals[1])

        self.input_viewers_widget_layout.addWidget(self.input_viewer1)
        self.input_viewers_widget_layout.addWidget(self.input_viewer2)

        self.output_viewer = OutputViewer(self.output_signal)
        self.viewers_widget_layout.addWidget(self.output_viewer)

        self.list_viewer = ListViewer()
        self.main_widget_layout.addWidget(self.list_viewer)
