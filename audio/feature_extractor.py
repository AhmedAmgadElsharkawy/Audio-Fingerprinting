import librosa
import numpy as np

class AudioFeatureExtractor:
    def extract_features(self, audio_file_path):
        y, sr = librosa.load(audio_file_path, duration=30)

        # Extract features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
        chroma_features = librosa.feature.chroma_cqt(y=y, sr=sr)
        tempo = librosa.beat.beat_track(y=y, sr=sr)

        return {
            'mfcc_mean': np.mean(mfccs, axis=1).tolist(),
            'mfcc_std': np.std(mfccs, axis=1).tolist(),
            'spectral_centroid_mean': float(np.mean(spectral_centroid)),
            'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
            'zero_crossing_rate_mean': float(np.mean(zero_crossing_rate)),
            'chroma_mean': np.mean(chroma_features, axis=1).tolist(),
            'tempo': float(tempo[0])
        }