import numpy as np
from scipy.io import wavfile
from PyQt5.QtMultimedia import QMediaPlayer

class OutputController():
    def __init__(self, output):
        self.output = output
        self.media_player = QMediaPlayer()
    
    def calc(self):
        volume1, volume2 = self.output.signal1_slider.signal_ratio_value / 100, self.output.signal2_slider.signal_ratio_value / 100
        self.play_mixed_audio(self.output.main_window.input_player1.audio_signal.file_path, self.output.main_window.input_player2.audio_signal.file_path, volume1, volume2)

    def play_mixed_audio(self, file1_path, file2_path, volume1, volume2):
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
                sample_rate, data2 = wavfile.read(file2_path)
                if not file1_path:
                    data1 = np.zeros_like(data2)
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
            self.output.file_path = temp_file_path

        except Exception as e:
            print(f"Error occurred while mixing or playing audio: {e}")

    def save_and_play_wav(self, modified_data, sample_rate): 
        modified_data_int16 = np.int16(modified_data / np.max(np.abs(modified_data)) * 32767) 
        output_file_path = "modified.wav" 
        wavfile.write(output_file_path, sample_rate, modified_data_int16) 
        return output_file_path