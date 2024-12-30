import numpy as np
from scipy.io import wavfile

class AudioMixer:
    def mix_audio_files(self, file1_path, file2_path, volume1, volume2):
        try:
            if not file1_path and not file2_path or volume1 == 0 and volume2 == 0:
                return None

            # Read first file
            sample_rate1, data1 = wavfile.read(file1_path) if file1_path else (44100, np.zeros(44100, dtype=np.int16))
            
            # Read second file
            sample_rate2, data2 = wavfile.read(file2_path) if file2_path else (sample_rate1, np.zeros_like(data1))
            
            # Convert to mono if needed
            data1 = data1.mean(axis=1).astype(np.int16) if len(data1.shape) > 1 else data1
            data2 = data2.mean(axis=1).astype(np.int16) if len(data2.shape) > 1 else data2

            # Adjust lengths
            min_length = min(len(data1), len(data2))
            data1 = data1[:min_length]
            data2 = data2[:min_length]

            # Mix with volumes
            mixed_data = (data1 * volume1 + data2 * volume2)
            mixed_data = np.clip(mixed_data, -32768, 32767)

            return mixed_data, sample_rate1

        except Exception as e:
            print(f"Error mixing audio: {e}")
            return None