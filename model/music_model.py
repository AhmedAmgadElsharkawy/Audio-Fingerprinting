import soundfile as sf
import numpy as np

class MusicModel:
    def __init__(self):
        self.file_path = None
        self.sample_rate = None
        self.time = None
        self.data = None
        
    def load_wav_data(self, file_path):
        try:
            self.file_path = file_path
            self.data, self.sample_rate = sf.read(file_path)
            self.time = np.arange(0, len(self.data)) / self.sample_rate
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return False
        return True