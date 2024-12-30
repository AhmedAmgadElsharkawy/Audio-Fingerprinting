import os
import json
import soundfile as sf
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
from audio.audio_mixer import AudioMixer
from audio.feature_extractor import AudioFeatureExtractor
from audio.similarity_calculator import SimilarityCalculator
from view.music_card import MusicCard
from view.image_display import ImageDisplay
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime

class OutputController:
    def __init__(self, output):
        self.output = output
        self.index = 0
        self.audio_mixer = AudioMixer()
        self.feature_extractor = AudioFeatureExtractor()
        self.similarity_calculator = SimilarityCalculator()

    def _mix_audio_files(self, volume1, volume2):
        mixed_data, sample_rate = self.audio_mixer.mix_audio_files(
            self.output.main_window.input_player1.filepath,
            self.output.main_window.input_player2.filepath,
            volume1,
            volume2
        )

        if mixed_data is None:
            return None

        # Create output directory if it doesn't exist
        os.makedirs('output/audio', exist_ok=True)

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join('output/audio', f'mixed_{timestamp}.wav')
        
        # Save mixed audio
        sf.write(output_path, mixed_data, sample_rate)
        
        self.output.filepath = output_path
        self.output.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(output_path))
        )
        
        return output_path

    def calc(self):
        if not self._validate_inputs():
            return

        # Get mixing ratios
        volume1 = self.output.signal1_slider.signal_ratio_value / 100
        volume2 = self.output.signal2_slider.signal_ratio_value / 100

        # Mix audio files and save
        mixed_path = self._mix_audio_files(volume1, volume2)
        if not mixed_path:
            return

        # Extract features and find similarities
        similarities = self._find_similarities(
            self.feature_extractor.extract_features(self.output.main_window.input_player1.filepath),
            self.feature_extractor.extract_features(self.output.main_window.input_player2.filepath),
            volume1,
            volume2
        )

        # Update UI with results
        self._update_ui_with_results(similarities)


    def _validate_inputs(self):
        return (self.output.main_window.input_player1.filepath and 
                self.output.main_window.input_player2.filepath)

    


    def _find_similarities(self, input1_features, input2_features, volume1, volume2):
        similarities = []
        features_dir = "data/Songs_Features"
        
        for file in os.listdir(features_dir):
            if not file.endswith("_fingerprint.txt"):
                continue
                
            with open(os.path.join(features_dir, file), 'r') as f:
                ref_data = json.load(f)
                ref_features = ref_data['features']
                
                # Calculate similarity with both input files
                similarity1 = self.similarity_calculator.calculate_similarity(
                    input1_features, 
                    ref_features
                )
                similarity2 = self.similarity_calculator.calculate_similarity(
                    input2_features,
                    ref_features
                )
                
                # Weight similarities based on mixing ratios
                weighted_similarity = (
                    similarity1 * volume1 + 
                    similarity2 * volume2
                ) / (volume1 + volume2 if volume1 + volume2 > 0 else 1)

                song_name = os.path.splitext(file)[0].replace('_fingerprint', '')
                similarities.append({
                    'name': song_name,
                    'similarity': weighted_similarity
                })
        
        return sorted(similarities, key=lambda x: x['similarity'], reverse=True)

    def _is_similar_title(self, title1, title2):
        # Remove spaces and convert to lowercase for comparison
        t1 = title1.lower().replace(' ', '')
        t2 = title2.lower().replace(' ', '')
        
        # Check if one is contained in the other or if they're very similar
        return t1 in t2 or t2 in t1 or (len(t1) > 0 and len(t2) > 0 and 
            (t1.startswith(t2) or t2.startswith(t1)))

    def _update_ui_with_results(self, similarities):
        # Clear existing cards
        for widget in self.output.main_window.music_list_viewer.findChildren(MusicCard):
            widget.deleteLater()
            
        seen_songs = []  # Track unique song names as a list to compare similarity
        card_count = 0
        
        # Update central image with top match
        if similarities and len(similarities) > 0:
            top_song = similarities[0]
            group_num = top_song['name'].split('_')[0]
            top_image_path = f"data/images/{group_num}.jpg"
            pixmap = QPixmap(top_image_path)
            if not pixmap.isNull():
                self.output.main_window.matched_song_cover.setPixmap(
                    pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                self.output.main_window.matched_song_cover.setAlignment(Qt.AlignCenter)
        
        # Add cards for unique matches
        for song in similarities:
            parts = song['name'].split('_')
            if len(parts) < 2:
                continue
                
            song_title = parts[1]
            
            # Check if we have a similar song title already
            is_duplicate = any(self._is_similar_title(song_title, existing) for existing in seen_songs)
            if is_duplicate:
                continue
                
            seen_songs.append(song_title)
            
            # Use the group number for the image path
            group_image_path = f"data/images/{parts[0]}.jpg"
            
            card = MusicCard(
                song_order=str(card_count + 1),
                album_cover_path=group_image_path,
                song_title=song_title,
                artist_name=parts[0],
                similarity_ratio_value=int(song['similarity'])
            )
            self.output.main_window.music_list_viewer.main_widget_layout.addWidget(card)
            
            card_count += 1
            if card_count >= 10:
                break

    def play_mixed_audio(self):
        if not self.output.filepath:
            return
        
        self.output.playing = not self.output.playing
        if self.output.playing:
            self.output.play_and_pause_button.setText("Pause")
            self.output.media_player.play()
        else:
            self.output.play_and_pause_button.setText("Play")
            self.output.media_player.pause()