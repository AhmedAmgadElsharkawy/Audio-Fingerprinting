from PyQt5.QtWidgets import QWidget,QHBoxLayout,QPushButton,QSlider,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from view.audio_player import AudioPlayer
from view.custom_slider import CustomSlider
from controller.output_controller import OutputController

class OutputPlayer(AudioPlayer):
    def __init__(self,main_window, audio_signal,header):
        super().__init__(header=header)
        self.audio_signal = audio_signal
        self.main_window = main_window
        self.output_controller = OutputController(self)
        self.setFixedHeight(260)
        self.playing = False
        self.filepath = None

        self.match_button = QPushButton("Match")
        self.controls_widget_layout.addWidget(self.match_button)
        self.match_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.sliders_widget = QWidget()
        self.sliders_widget_layout = QVBoxLayout(self.sliders_widget)
        self.sliders_widget_layout.setSpacing(10)
        self.sliders_widget.setObjectName("sliders_widget")
        self.main_widget_layout.addStretch()
        self.main_widget_layout.addWidget(self.sliders_widget)
        self.signal1_slider = CustomSlider("Song1 Ratio")
        self.signal2_slider = CustomSlider("Song2 Ratio")
        self.sliders_widget_layout.addWidget(self.signal1_slider)
        self.sliders_widget_layout.addWidget(self.signal2_slider)
        
        # Connect buttons to their handlers
        self.match_button.clicked.connect(self.mix)
        self.play_and_pause_button.clicked.disconnect(self.toggle_playing)
        self.play_and_pause_button.clicked.connect(self.play_mixed_song)

        # Initialize media player
        self.media_player = QMediaPlayer()
        self.media_player.stateChanged.connect(self.handle_media_state_changed)

        self.sliders_widget.setStyleSheet("""
            #sliders_widget{
                border:1px solid gray;
            }
        """)

    def mix(self):
        self.output_controller.calc()

    def play_mixed_song(self):
        if self.filepath:
            self.output_controller.play_mixed_audio()
        
    def handle_media_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.playing = False
            self.play_and_pause_button.setText("Play")