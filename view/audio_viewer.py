from PyQt5.QtWidgets import QPushButton,QFileDialog
import pyqtgraph as pg

class AudioViewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_signal)

    def play_signal(self):
        pass

        


