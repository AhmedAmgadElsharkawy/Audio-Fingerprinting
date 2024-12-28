from PyQt5.QtWidgets import QWidget,QHBoxLayout,QSlider,QVBoxLayout,QLabel
from PyQt5.QtCore import Qt

class CustomSlider(QWidget):
    def __init__(self, name):
        super().__init__()
        self.signal_ratio_value = 0
        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)

        self.main_widget = QWidget()
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.central_layout.addWidget(self.main_widget)

        self.bottom_container = QWidget()
        self.bottom_container_layout = QHBoxLayout(self.bottom_container)
        self.bottom_container_layout.setContentsMargins(0,0,0,0)

        self.signal_label = QLabel(name)
        self.signal_ratio_label = QLabel("0%")
        
        self.slider_container = QWidget()
        self.slider_container_layout = QHBoxLayout(self.slider_container)
        self.slider_container_layout.setContentsMargins(0,0,0,0)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)
        self.slider_container_layout.addWidget(self.slider)

        self.slider.setTickInterval(1) 

        self.main_widget_layout.addWidget(self.signal_label)
        self.bottom_container_layout.addWidget(self.slider_container)
        self.bottom_container_layout.addWidget(self.signal_ratio_label)
        self.main_widget_layout.addWidget(self.bottom_container)
        

        self.slider.valueChanged.connect(self.slider_change)
        

    def slider_change(self):
        self.signal_ratio_value = self.slider.value()
        self.signal_ratio_label.setText(f"{self.signal_ratio_value}%")
        

        