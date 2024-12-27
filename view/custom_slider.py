from PyQt5.QtWidgets import QWidget,QHBoxLayout,QSlider,QVBoxLayout,QLabel
from PyQt5.QtCore import Qt

class CustomSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)

        self.main_widget = QWidget()
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.central_layout.addWidget(self.main_widget)

        self.signal1_widget = QWidget()
        self.signal1_widget_layout = QVBoxLayout(self.signal1_widget)
        self.signal1_widget_layout.setContentsMargins(0,0,0,0)
        self.signal1_widget_layout.setSpacing(0)
        self.signal1_label = QLabel("Signal 1")
        self.signal1_ratio_label = QLabel("50%")
        self.signal1_label.setAlignment(Qt.AlignCenter)
        self.signal1_ratio_label.setAlignment(Qt.AlignCenter)

        self.signal1_widget_layout.addWidget(self.signal1_label)
        self.signal1_widget_layout.addWidget(self.signal1_ratio_label)
        
       
        self.signal2_widget = QWidget()
        self.signal2_widget_layout = QVBoxLayout(self.signal2_widget)
        self.signal2_widget_layout.setContentsMargins(0,0,0,0)
        self.signal2_widget_layout.setSpacing(0)
        self.signal2_label = QLabel("Signal 2")
        self.signal2_ratio_label = QLabel("50%")
        self.signal2_label.setAlignment(Qt.AlignCenter)
        self.signal2_ratio_label.setAlignment(Qt.AlignCenter)
        self.signal2_widget_layout.addWidget(self.signal2_label)
        self.signal2_widget_layout.addWidget(self.signal2_ratio_label)


        self.slider_container = QWidget()
        self.slider_container_layout = QHBoxLayout(self.slider_container)
        self.slider_container_layout.setContentsMargins(0,0,0,0)
        self.slider = QSlider()
        self.slider.setRange(-50, 50)
        self.slider.setValue(0)
        self.slider_container_layout.addWidget(self.slider)

        self.slider.setTickInterval(1) 

        
        self.main_widget_layout.addWidget(self.signal1_widget)
        self.main_widget_layout.addWidget(self.slider_container)
        self.main_widget_layout.addWidget(self.signal2_widget)

        