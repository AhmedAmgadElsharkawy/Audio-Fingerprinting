from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout
from view.audio_viewer import AudioViewer
from view.custom_slider import CustomSlider

class OutputViewer(QWidget):
    def __init__(self,audio_signal):
        super().__init__()
        self.audio_signal = audio_signal
        
        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_widget = QWidget()
        self.main_widget_layout = QHBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.central_layout.addWidget(self.main_widget)
        
        self.audio_viewer = AudioViewer()
        self.main_widget_layout.addWidget(self.audio_viewer)

        self.signals_ratio_slider = CustomSlider()
        self.main_widget_layout.addWidget(self.signals_ratio_slider)

        
    