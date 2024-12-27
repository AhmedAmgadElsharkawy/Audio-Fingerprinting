from PyQt5.QtWidgets import QPushButton,QWidget,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QIcon
import pyqtgraph as pg
from PyQt5.QtCore import QSize,Qt

class AudioViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.playing = False
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_widget = QWidget()
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.central_layout.addWidget(self.main_widget)
        
        
        self.plot = pg.PlotWidget()
        self.main_widget_layout.addWidget(self.plot)

        # self.plot_item.setBackground("w")
        self.plot.showGrid(x=True, y=True)
        # self.plot_item.getAxis('bottom').setPen(pg.mkPen('k'))  
        # self.plot_item.getAxis('left').setPen(pg.mkPen('k'))
        # self.plot_item.getAxis('bottom').setTextPen(pg.mkPen('k')) 
        # self.plot_item.getAxis('left').setTextPen(pg.mkPen('k')) 

        self.controls_widget = QWidget()
        self.controls_widget_layout = QHBoxLayout(self.controls_widget)
        self.main_widget_layout.addWidget(self.controls_widget)
        self.controls_widget_layout.setContentsMargins(0,0,0,0)
        self.controls_widget_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # self.play_icon = QIcon("assets/icons/play-button.png")  # Replace with your icon file path
        # self.pause_icon = QIcon("assets/icons/pause-button.png")

        self.play_and_pause_button = QPushButton("Play")
        self.play_and_pause_button.setFixedWidth(100)
        # self.play_and_pause_button.setIcon(self.play_icon)
        # self.play_and_pause_button.setIconSize(QSize(20, 20))  # Set icon size to 32x32
        # self.play_and_pause_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_and_pause_button.clicked.connect(self.toggle_icon)

        self.controls_widget_layout.addWidget(self.play_and_pause_button)

        self.play_and_pause_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        
        
        

    def toggle_icon(self):
        self.playing = not self.playing
        if self.playing:
            self.play_and_pause_button.setText("Pause")
            # self.play_and_pause_button.setIcon(self.pause_icon)
        else:
            self.play_and_pause_button.setText("Play")
            # self.play_and_pause_button.setIcon(self.play_icon)



        


