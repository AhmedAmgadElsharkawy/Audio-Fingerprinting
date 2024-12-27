from PyQt5.QtWidgets import QFileDialog
import pyqtgraph as pg
from view.audio_viewer import AudioViewer
from PyQt5.QtCore import Qt

class InputViewer(AudioViewer):
    def __init__(self):
        super().__init__()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Signal File", "", "Text Files (*.txt);;All Files (*)")
            
            if file_path:
                pass
    


        


