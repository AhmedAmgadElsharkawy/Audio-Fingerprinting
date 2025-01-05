from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from view.audio_player import AudioPlayer
from view.custom_slider import CustomSlider
from controller.output_controller import OutputController

class OutputPlayer(AudioPlayer):
    def __init__(self, main_window, audio_signal, header):
        super().__init__(header=header)
        self.audio_signal = audio_signal
        self.main_window = main_window
        self.output_controller = OutputController(self)
        self.setFixedHeight(260)
        self.playing = False
        self.filepath = None
        self.has_matched = False  # Track if match button was pressed

        # Add match button
        self.match_button = QPushButton("Match")
        self.controls_widget_layout.addWidget(self.match_button)
        self.match_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Disable buttons initially
        self.match_button.setEnabled(False)
        self.play_and_pause_button.setEnabled(False)

        self.sliders_widget = QWidget()
        self.sliders_widget_layout = QVBoxLayout(self.sliders_widget)
        self.sliders_widget.setObjectName("sliders_widget")
        self.main_widget_layout.addStretch()
        self.main_widget_layout.addWidget(self.sliders_widget)
        
        # Single slider for both songs
        self.mix_slider = CustomSlider()
        self.sliders_widget_layout.addWidget(self.mix_slider)
        
        # Connect buttons to their handlers
        self.match_button.clicked.connect(self.mix)
        self.play_and_pause_button.clicked.disconnect(self.toggle_playing)
        self.play_and_pause_button.clicked.connect(self.play_song)

        # Initialize media player
        self.media_player = QMediaPlayer()
        self.media_player.stateChanged.connect(self.handle_media_state_changed)

        self.sliders_widget.setStyleSheet("""
            #sliders_widget{
                border:1px solid gray;
            }
        """)

    def update_controls_state(self):
        has_input1 = bool(self.main_window.input_player1.filepath)
        has_input2 = bool(self.main_window.input_player2.filepath)
        
        # Enable match button if at least one song is uploaded
        self.match_button.setEnabled(has_input1 or has_input2)
        
        # Reset has_matched flag when songs change
        self.has_matched = False
        self.play_and_pause_button.setEnabled(False)
        
        # Update slider mode based on number of songs
        if has_input1 and has_input2:
            self.mix_slider.set_two_songs_mode()
        elif has_input1 or has_input2:
            self.mix_slider.set_single_song_mode()
        else:
            self.mix_slider.reset()

    def mix(self):
        has_input1 = bool(self.main_window.input_player1.filepath)
        has_input2 = bool(self.main_window.input_player2.filepath)

        if has_input1 and has_input2:
            # Mix both songs
            ratio = self.mix_slider.signal_ratio_value / 100
            self.output_controller.calc(ratio, 1 - ratio)
        elif has_input1:
            # Set media content for single song (input1)
            self.filepath = self.main_window.input_player1.filepath
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.filepath)))
            self.output_controller.calc(1, 0)
        elif has_input2:
            # Set media content for single song (input2)
            self.filepath = self.main_window.input_player2.filepath
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.filepath)))
            self.output_controller.calc(1, 0)
        
        # Enable play button after matching
        self.has_matched = True
        self.play_and_pause_button.setEnabled(True)

    def play_song(self):
        if not self.has_matched:
            return

        if not self.playing:
            self.playing = True
            self.play_and_pause_button.setText("Pause")
            self.media_player.play()
        else:
            self.playing = False
            self.play_and_pause_button.setText("Play")
            self.media_player.pause()
        
    def handle_media_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.playing = False
            self.play_and_pause_button.setText("Play")