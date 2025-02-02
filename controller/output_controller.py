import os
import json
import soundfile as sf
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtGui import QPixmap
from audio.audio_mixer import AudioMixer
from audio.feature_extractor import AudioFeatureExtractor
from audio.similarity_calculator import SimilarityCalculator
from view.music_card import MusicCard  

class OutputController:
    def __init__(self, output):
        self.output = output
        self.index = 0
        self.audio_mixer = AudioMixer()
        self.feature_extractor = AudioFeatureExtractor()
        self.similarity_calculator = SimilarityCalculator()
        
        # Create necessary directories
        os.makedirs('output/audio', exist_ok=True)
        os.makedirs('output/features', exist_ok=True)

    def calc(self, volume1, volume2):
        # Check which input files are available
        has_input1 = bool(self.output.main_window.input_player1.filepath)
        has_input2 = bool(self.output.main_window.input_player2.filepath)

        if not has_input1 and not has_input2:
            print("No input files selected")
            return

        if has_input1 and has_input2:
            self._handle_mixed_songs(volume1, volume2)
        else:
            self._handle_single_song(
                self.output.main_window.input_player1.filepath or 
                self.output.main_window.input_player2.filepath
            )

    def _handle_single_song(self, input_path):
        # Extract features from the input file
        input_features = self.feature_extractor.extract_features(input_path)
        
        # Find similarities without mixing
        similarities = self._find_similarities_single(input_features)
        
        # Update UI with results
        self._update_ui_with_results(similarities)
        
        # Update the central image with the top match
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

    def _handle_mixed_songs(self, volume1, volume2):
        # Extract features from both input files
        input1_features = self.feature_extractor.extract_features(
            self.output.main_window.input_player1.filepath
        )
        input2_features = self.feature_extractor.extract_features(
            self.output.main_window.input_player2.filepath
        )

        # Mix audio files and save
        mixed_path = self._mix_and_save_audio(volume1, volume2)
        if not mixed_path:
            return

        # Extract and save features of mixed audio
        mixed_features = self.feature_extractor.extract_features(mixed_path)
        self._save_features(mixed_features, f'mixed_song_{self.index}')

        # Find similarities for mixed audio
        similarities = self._find_similarities(
            input1_features, 
            input2_features,
            volume1,
            volume2
        )

        # Update UI with results
        self._update_ui_with_results(similarities)

    def _find_similarities_single(self, input_features):
        similarities = []
        features_dir = "data/Songs_Features"
        
        for file in os.listdir(features_dir):
            if not file.endswith("_fingerprint.txt"):
                continue
                
            with open(os.path.join(features_dir, file), 'r') as f:
                ref_data = json.load(f)
                ref_features = ref_data['features']
                
                # Calculate similarity with the single input file
                similarity = self.similarity_calculator.calculate_similarity(
                    input_features, 
                    ref_features
                )

                song_name = os.path.splitext(file)[0].replace('_fingerprint', '')
                similarities.append({
                    'name': song_name,
                    'similarity': similarity
                })
        
        return sorted(similarities, key=lambda x: x['similarity'], reverse=True)

    def _mix_and_save_audio(self, volume1, volume2):
        mixed_data, sample_rate = self.audio_mixer.mix_audio_files(
            self.output.main_window.input_player1.filepath,
            self.output.main_window.input_player2.filepath,
            volume1,
            volume2
        )

        if mixed_data is None:
            return None

        # Increment index for next mixed song
        self.index += 1
        
        # Save with sequential naming
        output_path = os.path.join('output/audio', f'mixed_song_{self.index}.wav')
        sf.write(output_path, mixed_data, sample_rate)
        
        self.output.filepath = output_path
        self.output.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(output_path))
        )
        
        return output_path

    def _save_features(self, features, filename):
        """Save audio features to txt file"""
        feature_path = os.path.join('output/features', f"{filename}_features.txt")
        with open(feature_path, 'w') as f:
            json.dump(features, f, indent=2)

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