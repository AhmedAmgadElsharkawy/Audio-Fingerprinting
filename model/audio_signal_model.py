import numpy as np
from scipy.io import wavfile

class AudioSignalModel():
    def __init__(self):
        self.file_path = None
        self.sample_rate = None
        self.time = None
        self.data = None

    def load_wav_data(self,file_path):
        self.file_path = file_path
        self.sample_rate, self.data = wavfile.read(file_path)
        self.time = np.arange(0, len(self.data)) / self.sample_rate
