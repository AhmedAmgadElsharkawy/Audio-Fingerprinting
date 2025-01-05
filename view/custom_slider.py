from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class CustomSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.signal_ratio_value = 50  # Start at 50-50 for no songs
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)

        # Song labels container
        self.song_labels = QWidget()
        self.song_labels_layout = QHBoxLayout(self.song_labels)
        self.song_labels_layout.setContentsMargins(0,0,0,0)
        
        # Song labels
        self.song1_label = QLabel("Song 1")
        self.song2_label = QLabel("Song 2")
        self.song1_label.setAlignment(Qt.AlignLeft)
        self.song2_label.setAlignment(Qt.AlignRight)
        
        self.song_labels_layout.addWidget(self.song1_label)
        self.song_labels_layout.addStretch()
        self.song_labels_layout.addWidget(self.song2_label)

        # Slider
        self.slider_container = QWidget()
        self.slider_container_layout = QHBoxLayout(self.slider_container)
        self.slider_container_layout.setContentsMargins(0,0,0,0)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.setEnabled(False)  # Disabled by default
        self.slider_container_layout.addWidget(self.slider)

        # Volume labels container
        self.volume_container = QWidget()
        self.volume_layout = QHBoxLayout(self.volume_container)
        self.volume_layout.setContentsMargins(0,0,0,0)
        
        # Volume labels
        self.volume1_label = QLabel("50%")
        self.volume2_label = QLabel("50%")
        self.volume1_label.setAlignment(Qt.AlignLeft)
        self.volume2_label.setAlignment(Qt.AlignRight)
        
        self.volume_layout.addWidget(self.volume1_label)
        self.volume_layout.addStretch()
        self.volume_layout.addWidget(self.volume2_label)

        # Add widgets to main layout
        self.central_layout.addWidget(self.song_labels)
        self.central_layout.addWidget(self.slider_container)
        self.central_layout.addWidget(self.volume_container)

        self.slider.valueChanged.connect(self.slider_change)

    def slider_change(self):
        self.signal_ratio_value = self.slider.value()
        self.volume1_label.setText(f"{self.signal_ratio_value}%")
        self.volume2_label.setText(f"{100-self.signal_ratio_value}%")

    def set_single_song_mode(self):
        self.slider.setValue(100)
        self.slider.setEnabled(False)

    def set_two_songs_mode(self):
        self.slider.setValue(50)
        self.slider.setEnabled(True)

    def reset(self):
        self.slider.setValue(50)
        self.slider.setEnabled(False)