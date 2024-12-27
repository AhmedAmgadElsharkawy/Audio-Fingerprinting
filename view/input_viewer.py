from PyQt5.QtWidgets import QFileDialog,QPushButton
from view.audio_viewer import AudioViewer
from PyQt5.QtCore import Qt


class InputViewer(AudioViewer):
    def __init__(self,audio_signal):
        super().__init__()
        self.audio_signal = audio_signal
        self.upload_signal_button = QPushButton("Upload")
        self.upload_signal_button.setFixedWidth(100)
        self.controls_widget_layout.addWidget(self.upload_signal_button)
        self.upload_signal_button.clicked.connect(self.uploadSignal)
        self.upload_signal_button.setCursor(Qt.CursorShape.PointingHandCursor)

    def uploadSignal(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open .wav", "", "*.wav")
        if file_path:
            self.audio_signal.load_wav_data(file_path)

        


