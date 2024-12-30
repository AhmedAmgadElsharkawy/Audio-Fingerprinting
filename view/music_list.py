from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from view.music_card import MusicCard

class MusicList(QWidget):
    def __init__(self, songs_list):
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

        # Default song data
        self.default_songs = [
            {"title": "Save Your Tears", "artist": "Group1", "image": "data/images/1.jpg"},
            {"title": "Let Her Go", "artist": "Group13", "image": "data/images/13.jpg"},
            {"title": "Please", "artist": "Group9", "image": "data/images/9.jpg"},
            {"title": "NinaCriedPower", "artist": "Group5", "image": "data/images/5.jpg"},
            {"title": "Ya Lala", "artist": "Group15", "image": "data/images/15.jpg"},
            {"title": "Wen Elkhael", "artist": "Group10", "image": "data/images/10.jpg"},
            {"title": "SomeLikeYou", "artist": "Group3", "image": "data/images/3.jpg"},
            {"title": "A Thousand Years", "artist": "Group8", "image": "data/images/8.jpg"},
            {"title": "FEIN", "artist": "Group11", "image": "data/images/11.jpg"},
            {"title": "A Sky Full of Stars", "artist": "Group14", "image": "data/images/14.jpg"}
        ]

        self.load_default_songs()

        self.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #2A2A2A;  
                width: 7px;
                margin: 0px;
                border-radius: 5px;
                border-radius: 3px;
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

    def load_default_songs(self):
        # Clear existing cards
        for i in reversed(range(self.main_widget_layout.count())): 
            self.main_widget_layout.itemAt(i).widget().setParent(None)
            
        # Add default songs
        for i, song in enumerate(self.default_songs):
            music_card = MusicCard(
                song_order=str(i + 1),
                album_cover_path=f"data/images/{song['artist']}.jpg",
                song_title=song["title"],
                artist_name=song["artist"],
                similarity_ratio_value=0  # Start with 0%
            )
            self.main_widget_layout.addWidget(music_card)

    def update_songs(self, similarities):
        # Clear existing cards
        for i in reversed(range(self.main_widget_layout.count())): 
            self.main_widget_layout.itemAt(i).widget().setParent(None)
            
        # Add new cards based on similarities
        for i, song in enumerate(similarities[:10]):  # Limit to 10 songs
            music_card = MusicCard(
                song_order=str(i + 1),
                album_cover_path=f"data/images/{song['artist']}.jpg",
                song_title=song['title'],
                artist_name=song['artist'],
                similarity_ratio_value=int(song['similarity'])
            )
            self.main_widget_layout.addWidget(music_card)