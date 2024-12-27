from PyQt5.QtWidgets import QFileDialog
from view.audio_viewer import AudioViewer
from PyQt5.QtCore import Qt


class InputViewer(AudioViewer):
    def __init__(self,audio_signal):
        super().__init__()
        self.audio_signal = audio_signal


    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open .wav", "", "*.wav")
            if file_path:
                self.audio_signal.load_wav_data(file_path)

        


