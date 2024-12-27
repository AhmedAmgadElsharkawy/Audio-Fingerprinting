import numpy as np
from scipy.io import wavfile

class AudioSignalModel():
    def __init__(self):
        self.file_path = None
        self.file_extension = None
        self.sample_rate = None
        self.time = None
        self.data = None

    def load_wav_data(self,file_path,file_extension):
        self.file_path = file_path
        self.file_extension = file_extension
        self.sample_rate, self.data = wavfile.read(file_path)
        self.time = np.arange(0, len(self.data)) / self.sample_rate
        self.calculate_data()