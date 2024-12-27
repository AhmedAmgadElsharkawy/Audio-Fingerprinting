from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSlider, QVBoxLayout, QLabel, QScrollArea
class ListViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_widget = QWidget()
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.main_widget)
        self.scroll_area.setWidgetResizable(True)  # Make the widget inside scrollable

        self.central_layout.addWidget(self.scroll_area)
