from PyQt5.QtCore import QUrl
import os
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QFileDialog

class InputController():
    def __init__(self, input_winodw):
        self.input_window = input_winodw

    def uploadSignal(self):
        file_path, _ = QFileDialog.getOpenFileName(self.input_window, "Open .wav", "", "*.wav")
        self.input_window.filepath = file_path
        self.input_window.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.input_window.filepath)))
        file_name = os.path.basename(file_path)
        self.input_window.header_label.setText(file_name)
        if file_path:
            self.input_window.audio_signal.load_wav_data(file_path)