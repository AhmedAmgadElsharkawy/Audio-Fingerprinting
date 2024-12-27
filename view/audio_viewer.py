from PyQt5.QtWidgets import QPushButton,QFileDialog
from PyQt5.QtGui import QIcon
import pyqtgraph as pg
from PyQt5.QtCore import QSize,Qt

class AudioViewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground("w")
        self.showGrid(x=True, y=True)
        self.getAxis('bottom').setPen(pg.mkPen('k'))  
        self.getAxis('left').setPen(pg.mkPen('k'))
        self.getAxis('bottom').setTextPen(pg.mkPen('k')) 
        self.getAxis('left').setTextPen(pg.mkPen('k')) 

        self.play_icon = QIcon("assets/icons/play-button.png")  # Replace with your icon file path
        self.pause_icon = QIcon("assets/icons/pause-button.png")

        self.button = QPushButton(parent = self)
        self.set_play_icon()
        self.button.setGeometry(50,30,40,40)
        self.button.setIconSize(QSize(40, 40))  # Set icon size to 32x32
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: none; /* Optional: hover effect */
            }
        """)

    def set_pause_icon(self):
        self.button.setIcon(self.pause_icon)

    def set_play_icon(self):
        self.button.setIcon(self.play_icon)



        


