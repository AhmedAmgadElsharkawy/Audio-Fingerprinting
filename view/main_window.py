from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from view.input_player import InputPlayer
from view.output_player import OutputPlayer

from model.audio_signal_model import AudioSignalModel

from view.music_list import MusicList



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fingerprint')
        self.setFixedSize(800, 500)

        self.input_signals = [AudioSignalModel(),AudioSignalModel()]
        self.output_signal = AudioSignalModel()

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QHBoxLayout(self.main_widget)

        self.viewers_widget = QWidget()
        self.viewers_widget.setObjectName("viewers_widget")
        self.viewers_widget.setObjectName("viewers_widget")
        self.viewers_widget_layout = QVBoxLayout(self.viewers_widget)
        self.viewers_widget_layout.setContentsMargins(0,0,0,0)
        self.viewers_widget_layout.setSpacing(20)
        
        self.main_widget_layout.addWidget(self.viewers_widget)

        # self.matched_song_cover = QLabel()
        # self.main_widget_layout.addWidget(self.matched_song_cover)
        # pixmap = QPixmap("data/music/song1/song_img.jpeg")  # Replace with the image path
        # self.matched_song_cover.setPixmap(pixmap.scaled(500, 700, Qt.KeepAspectRatio))  # Scale the image
        # self.matched_song_cover.setAlignment(Qt.AlignCenter)
        


        self.input_viewer1 = InputPlayer(self.input_signals[0],header="Song 1")
        self.input_viewer2 = InputPlayer(self.input_signals[1],header="Song 1")

        self.viewers_widget_layout.addWidget(self.input_viewer1)
        self.viewers_widget_layout.addWidget(self.input_viewer2)

        self.output_viewer = OutputPlayer(self.output_signal,header="Mixed Audio")
        self.viewers_widget_layout.addStretch()
        self.viewers_widget_layout.addWidget(self.output_viewer)

        self.list_viewer = MusicList()
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
                height: 10px;
                background: #444;
                margin: 0px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: rgb(4,124,212);
                width: 12px;
                height: 8px;
                border-radius: 6px;
                margin: -4px 0;
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
