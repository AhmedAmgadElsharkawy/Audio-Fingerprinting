from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea,QGridLayout
from PyQt5.QtCore import Qt

from view.music_card import MusicCard
class MusicList(QWidget):
    def __init__(self,songs_list):
        super().__init__()
        self.setFixedWidth(500)
        self.songs_list = songs_list
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_widget = QWidget()
        self.main_widget.setObjectName("list_viewer_main_widget")
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setSpacing(12)
        self.main_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_widget_layout.setContentsMargins(10,5,10,5)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.main_widget)
        self.scroll_area.setWidgetResizable(True) 

        self.central_layout.addWidget(self.scroll_area)

        self.load_music_cards()

    
        self.setStyleSheet("""

            QScrollArea {
                border:none;
            }
            QScrollBar:vertical {
                border: none;
                background: #2A2A2A;  
                width: 7px;
                margin: 0px;
                border-radius: 5px;
                border-radius:3px;
            }
            QScrollBar::handle:vertical {
                background: #047cdc;
                min-height: 15px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
            }
            QScrollBar::handle:vertical:hover {
                background: #0056b3;
            }
        """)


    def load_music_cards(self):
        for i,song in enumerate(self.songs_list):
            music_card = MusicCard(song_order=str(i+1),artist_name="The Weeknd",album_cover_path="data/music/song1/song_img.jpeg",song_title="save your tears",similarity_ratio_value = 50)
            self.main_widget_layout.addWidget(music_card)
            

        
