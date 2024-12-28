from PyQt5.QtWidgets import QFileDialog,QPushButton,QLabel
from view.audio_player import AudioPlayer
from PyQt5.QtCore import Qt


class InputPlayer(AudioPlayer):
    def __init__(self,audio_signal,header):
        super().__init__(header=header)
        self.audio_signal = audio_signal
        self.upload_signal_button = QPushButton("Upload")
        self.controls_widget_layout.addWidget(self.upload_signal_button)
        self.upload_signal_button.clicked.connect(self.uploadSignal)
        self.upload_signal_button.setCursor(Qt.CursorShape.PointingHandCursor)




    def uploadSignal(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open .wav", "", "*.wav")
        if file_path:
            self.audio_signal.load_wav_data(file_path)

        


