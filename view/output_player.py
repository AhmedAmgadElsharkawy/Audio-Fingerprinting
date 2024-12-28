from PyQt5.QtWidgets import QWidget,QHBoxLayout,QPushButton,QSlider,QVBoxLayout
from PyQt5.QtCore import Qt

from view.audio_player import AudioPlayer
from view.custom_slider import CustomSlider


class OutputPlayer(AudioPlayer):
    def __init__(self,audio_signal,header):
        super().__init__(header=header)
        self.audio_signal = audio_signal

        self.match_button = QPushButton("Match")
        self.controls_widget_layout.addWidget(self.match_button)
        self.match_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.sliders_widget = QWidget()
        self.sliders_widget_layout = QVBoxLayout(self.sliders_widget)
        self.sliders_widget_layout.setContentsMargins(0,0,0,0)
        self.controls_widget_layout.addWidget(self.sliders_widget)
        self.signal1_slider = CustomSlider("S1")
        self.signal2_slider = CustomSlider("S2")
        self.sliders_widget_layout.addWidget(self.signal1_slider)
        self.sliders_widget_layout.addWidget(self.signal2_slider)
        

        




        
    