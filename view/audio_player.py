from PyQt5.QtWidgets import QPushButton,QWidget,QVBoxLayout,QHBoxLayout,QLabel
from PyQt5.QtGui import QIcon
import pyqtgraph as pg
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from controller.audio_player_controller import AudioPlayerController


class AudioPlayer(QWidget):
    def __init__(self,header):
        super().__init__()
        self.playing = False
        self.filepath = None
        self.main_window = None
        self.prevent_recursion = False
        self.audio_player_controller = AudioPlayerController(self)
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_widget = QWidget()
        self.main_widget.setObjectName("viewer_main_widget")
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setSpacing(15)
        self.central_layout.addWidget(self.main_widget)
        
        self.header_label = QLabel(header)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.main_widget_layout.addWidget(self.header_label)


        self.controls_widget = QWidget()
        self.controls_widget_layout = QVBoxLayout(self.controls_widget)
        self.controls_widget_layout.setContentsMargins(0,0,0,0)
        self.controls_widget.setObjectName("viewer_controls_widget")
        self.main_widget_layout.addWidget(self.controls_widget)
        self.play_and_pause_button = QPushButton("Play")

        self.play_and_pause_button.clicked.connect(self.toggle_playing)

        self.controls_widget_layout.addWidget(self.play_and_pause_button)

        self.play_and_pause_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.media_player = QMediaPlayer()
        
        self.setStyleSheet("""
        #viewer_main_widget{
            border:1px solid gray;
            border-radius:5px;                   
        }
""")
        
    def toggle_playing(self):
        self.audio_player_controller.toggle_playing()

    def toggle_other_file(self):
        self.audio_player_controller.toggle_other_file()
