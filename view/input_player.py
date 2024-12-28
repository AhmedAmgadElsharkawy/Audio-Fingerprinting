from PyQt5.QtWidgets import QPushButton
from view.audio_player import AudioPlayer
from controller.input_controller import InputController
from PyQt5.QtCore import Qt

class InputPlayer(AudioPlayer):
    def __init__(self,main_window, audio_signal,header):
        super().__init__(header=header)
        self.audio_signal = audio_signal
        self.main_window = main_window
        self.input_contoller = InputController(self)
        self.upload_signal_button = QPushButton("Upload")
        self.controls_widget_layout.addWidget(self.upload_signal_button)
        self.upload_signal_button.clicked.connect(self.uploadSignal)
        self.upload_signal_button.setCursor(Qt.CursorShape.PointingHandCursor)

    def uploadSignal(self):
        self.input_contoller.uploadSignal()
