from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout

from view.input_viewer import InputViewer
from view.output_viewer import OutputViewer

from model.audio_signal_model import AudioSignalModel

from view.list_viewer import ListViewer



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FT-Mixer')
        self.setGeometry(200, 100, 1200, 600)

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

            QSlider::groove:vertical {
                background: #444;
                width: 10px;
                border-radius: 5px; 
                margin: 0px;
            }
            QSlider::handle:vertical {
                background: rgb(4,124,212); /* Blue color */
                width: 16px; /* Increased handle size */
                height: 16px; /* Keep handle size proportional */
                border-radius: 10px; /* Ensure circular handle */
                margin: -10px; /* Center the handle in the groove */
                border: 2px solid #2a2a2a; /* Add border to enhance visibility */
            }
            QSlider::handle:vertical:hover {
                background: #007BFF; /* Slightly lighter blue when hovered */
            }
            QSlider::handle:vertical:disabled {
                background: #555;
                border: 2px solid #444;
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
