import numpy as np
from scipy.io import wavfile
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import imagehash
from PIL import Image
import io

class OutputController():
    def __init__(self, output):
        self.output = output
        self.media_player = QMediaPlayer()
    
    def calc(self):
        volume1, volume2 = self.output.signal1_slider.signal_ratio_value / 100, self.output.signal2_slider.signal_ratio_value / 100
        self.mix_audios(self.output.main_window.input_player1.audio_signal.file_path, self.output.main_window.input_player2.audio_signal.file_path, volume1, volume2)

    def mix_audios(self, file1_path, file2_path, volume1, volume2):
        try:
            if not file1_path and not file2_path or volume1 == 0 and volume2 == 0:
                return
            
            sample_rate = -1
            data1, data2 = 0, 0

            if file1_path:
                sample_rate, data1 = wavfile.read(file1_path)
            else:
                sample_rate = 44100
                data1 = np.zeros(44100, dtype=np.int16)

            if file2_path:
                temp = sample_rate
                sample_rate, data2 = wavfile.read(file2_path)
                if not file1_path:
                    data1 = np.zeros_like(data2)
                else:
                    sample_rate = (sample_rate + temp) // 2
            else:
                data2 = np.zeros_like(data1)

            if len(data1.shape) > 1:
                data1 = data1.mean(axis=1).astype(np.int16)
            if len(data2.shape) > 1:
                data2 = data2.mean(axis=1).astype(np.int16)

            min_length = min(len(data1), len(data2))
            data1 = data1[:min_length]
            data2 = data2[:min_length]

            data1 = data1 * volume1
            data2 = data2 * volume2

            data1 = np.clip(data1, -32768, 32767)
            data2 = np.clip(data2, -32768, 32767)

            mixed_data = data1 + data2
            mixed_data = np.clip(mixed_data, -32768, 32767)

            temp_file_path = self.save_and_play_wav(mixed_data, sample_rate)
            self.output.filepath = temp_file_path
            self.output.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.output.filepath)))
            self.process_audio_file()

        except Exception as e:
            print(f"Error occurred while mixing or playing audio: {e}")

    def save_and_play_wav(self, modified_data, sample_rate): 
        modified_data_int16 = np.int16(modified_data / np.max(np.abs(modified_data)) * 32767) 
        output_file_path = "modified.wav" 
        wavfile.write(output_file_path, sample_rate, modified_data_int16) 
        return output_file_path
    
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
    
    def extract_audio_features(self, audio_file_path):
        y, sr = librosa.load(audio_file_path, duration=30)  

        # Extract features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
        chroma_features = librosa.feature.chroma_cqt(y=y, sr=sr)
        tempo = librosa.beat.beat_track(y=y, sr=sr)

        # Calculate mean and standard deviation of features
        mfcc_mean = np.mean(mfccs, axis=1).tolist()  
        mfcc_std = np.std(mfccs, axis=1).tolist()
        spectral_centroid_mean = float(np.mean(spectral_centroid))
        spectral_rolloff_mean = float(np.mean(spectral_rolloff))
        zero_crossing_rate_mean = float(np.mean(zero_crossing_rate))
        chroma_mean = np.mean(chroma_features, axis=1).tolist()

        features = {
            'mfcc_mean': mfcc_mean,
            'mfcc_std': mfcc_std,
            'spectral_centroid_mean': spectral_centroid_mean,
            'spectral_rolloff_mean': spectral_rolloff_mean,
            'zero_crossing_rate_mean': zero_crossing_rate_mean,
            'chroma_mean': chroma_mean,
            'tempo': float(tempo[0])  # Fixed tempo extraction
        }
        return features

    def normalize_array(self, arr):
        arr = np.array(arr)
        min_val = np.min(arr)
        max_val = np.max(arr)
        if max_val == min_val:
            return np.zeros_like(arr)
        return (arr - min_val) / (max_val - min_val)

    def normalize_value(self, val):
        return float(val) / (1 + abs(float(val)))

    def generate_audio_fingerprint(self, features):
        # Get the size of MFCC features to use as reference
        mfcc_size = len(features['mfcc_mean'])
        
        # Interpolate chroma features to match MFCC size
        chroma_interpolated = np.interp(
            np.linspace(0, 1, mfcc_size),
            np.linspace(0, 1, len(features['chroma_mean'])),
            self.normalize_array(features['chroma_mean'])
        )
        
        feature_matrix = np.vstack([
            self.normalize_array(features['mfcc_mean']).reshape(1, -1),
            self.normalize_array(features['mfcc_std']).reshape(1, -1),
            np.full((1, mfcc_size), self.normalize_value(features['spectral_centroid_mean'])),
            np.full((1, mfcc_size), self.normalize_value(features['spectral_rolloff_mean'])),
            np.full((1, mfcc_size), self.normalize_value(features['zero_crossing_rate_mean'])),
            chroma_interpolated.reshape(1, -1),
            np.full((1, mfcc_size), self.normalize_value(features['tempo']))
        ])
        
        plt.figure(figsize=(8, 8))
        plt.imshow(feature_matrix, cmap='viridis', aspect='auto')
        plt.axis('off')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        image = Image.open(buf)
        hash_value = str(imagehash.average_hash(image))
        
        return {
            'features': features,
            'hash': hash_value
        }

    def process_audio_file(self):
        audio_file = self.output.filepath
        try:
            # Extract features
            features = self.extract_audio_features(audio_file)
            
            # Generate fingerprint with hash
            fingerprint = self.generate_audio_fingerprint(features)
            
            # Save features and hash to file
            output_filename = os.path.splitext(audio_file)[0] + '_fingerprint.txt'

            with open(output_filename, 'w') as f:
                json.dump(fingerprint, f, indent=4)
                
            print(f"Processed {audio_file} -> {output_filename}")
            
        except Exception as e:
            print(f"Error processing {audio_file}: {str(e)}")
                