from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout

from view.input_viewer import InputViewer
from view.output_viewer import OutputViewer

from model.audio_signal_model import AudioSignalModel

from view.list_viewer import ListViewer



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FT-Mixer')
        self.setGeometry(300, 100, 1400, 900)

        self.input_signals = [AudioSignalModel(),AudioSignalModel()]
        self.output_signal = AudioSignalModel()

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QHBoxLayout(self.main_widget)

        self.viewers_widget = QWidget()
        self.viewers_widget_layout = QVBoxLayout(self.viewers_widget)
        
        self.main_widget_layout.addWidget(self.viewers_widget)
        
        # self.input_viewers_widget = QWidget()
        # self.input_viewers_widget_layout = QHBoxLayout(self.input_viewers_widget)
        # self.viewers_widget_layout.addWidget(self.input_viewers_widget)


        self.input_viewer1 = InputViewer(self.input_signals[0])
        self.input_viewer2 = InputViewer(self.input_signals[1])

        self.viewers_widget_layout.addWidget(self.input_viewer1)
        self.viewers_widget_layout.addWidget(self.input_viewer2)

        self.output_viewer = OutputViewer(self.output_signal)
        self.viewers_widget_layout.addWidget(self.output_viewer)

        self.list_viewer = ListViewer()
        self.main_widget_layout.addWidget(self.list_viewer)

        self.setStyleSheet("""
            * {
                background-color: #121212;
                color: #E0E0E0;
                font-family: Arial;
            }
            QMainWindow {
                background-color: #121212;
            }
            QWidget {
                background-color: #1E1E1E;
            }
            QLabel {
                color: #E0E0E0;
                font-weight: bold;
                border: none;
            }

            QPushButton {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #444;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #252525;
            }
            QPushButton:disabled {
                background-color: #3E3E3E;
                color: #777;
                border: 1px solid #555;
            }

            QSlider::groove:horizontal {
                height: 15px;
                background: #444;
                margin: 0px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: rgb(4,124,212);
                width: 16px;
                height: 12px;
                border-radius: 6px;
                margin: -5px 0;
                border: 1px solid #2a2a2a;
            }
            QSlider::handle:horizontal:hover {
                background: #777;
            }
            QSlider::handle:horizontal:disabled {
                background: #555;
                border: 1px solid #444;
            }

            QProgressBar {
                text-align: center;
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                background-color: #444;
            }
            QProgressBar::chunk {
                background-color: rgb(4,124,212);
                border-radius: 4px;
            }
        """)
