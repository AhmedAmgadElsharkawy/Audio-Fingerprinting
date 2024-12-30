from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MusicCard(QWidget):
    def __init__(self, song_order, album_cover_path, song_title, artist_name, similarity_ratio_value):
        super().__init__()
        self.setFixedHeight(60)
        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)

        self.main_widget = QWidget()
        self.main_widget_layout = QHBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)

        self.central_layout.addWidget(self.main_widget)

        self.music_info_widget = QWidget()
        self.music_info_wiget_layout = QHBoxLayout(self.music_info_widget)
        self.music_info_wiget_layout.setContentsMargins(0,0,0,0)

        # Order number
        self.order_label = QLabel(song_order)
        self.order_label.setFixedWidth(25)
        self.order_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.order_label.setStyleSheet("font-size: 20px;")

        # Album cover
        self.album_cover = QLabel()
        pixmap = QPixmap(album_cover_path)
        if not pixmap.isNull():
            self.album_cover.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.album_cover.setFixedSize(60, 60)
        self.album_cover.setAlignment(Qt.AlignCenter)

        # Song info
        self.song_title = QLabel(song_title)
        self.artist_name = QLabel(artist_name)
        self.song_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.artist_name.setStyleSheet("font-size: 12px; color: gray;")

        self.text_widget = QWidget()
        self.text_widget_layout = QVBoxLayout(self.text_widget)
        self.text_widget_layout.addWidget(self.song_title)
        self.text_widget_layout.addWidget(self.artist_name)

        # Add widgets to layouts
        self.music_info_wiget_layout.addWidget(self.order_label)
        self.music_info_wiget_layout.addWidget(self.album_cover)
        self.music_info_wiget_layout.addWidget(self.text_widget)

        self.main_widget_layout.addWidget(self.music_info_widget)

        # Similarity ratio bar
        self.similarity_ratio_bar = QProgressBar()
        self.similarity_ratio_bar.setFixedWidth(150)
        self.similarity_ratio_bar.setRange(0, 100)
        self.similarity_ratio_bar.setTextVisible(True)
        self.similarity_ratio_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.similarity_ratio_bar.setValue(similarity_ratio_value)
        self.main_widget_layout.addStretch()
        self.main_widget_layout.addWidget(self.similarity_ratio_bar)