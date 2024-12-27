from PyQt5.QtWidgets import QWidget,QHBoxLayout,QPushButton
from PyQt5.QtCore import Qt

from view.audio_viewer import AudioViewer
from view.custom_slider import CustomSlider


class OutputViewer(AudioViewer):
    def __init__(self,audio_signal):
        super().__init__()
        self.audio_signal = audio_signal

        self.match_button = QPushButton("Match")
        self.controls_widget_layout.addWidget(self.match_button)
        self.match_button.setFixedWidth(100)
        self.match_button.setCursor(Qt.CursorShape.PointingHandCursor)
                
        self.signals_ratio_slider = CustomSlider()
        self.controls_widget_layout.addWidget(self.signals_ratio_slider)




        
    