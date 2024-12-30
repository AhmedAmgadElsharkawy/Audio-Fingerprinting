import numpy as np
import soundfile as sf

class AudioMixer:
    def mix_audio_files(self, file1_path, file2_path, volume1, volume2):
        try:
            if not file1_path and not file2_path or volume1 == 0 and volume2 == 0:
                return None

            # Read audio files using soundfile
            data1, sample_rate1 = sf.read(file1_path) if file1_path else (np.zeros(44100), 44100)
            data2, sample_rate2 = sf.read(file2_path) if file2_path else (np.zeros_like(data1), sample_rate1)

            # Convert to mono if needed
            data1 = data1.mean(axis=1) if len(data1.shape) > 1 else data1
            data2 = data2.mean(axis=1) if len(data2.shape) > 1 else data2

            # Ensure same sample rate
            if sample_rate1 != sample_rate2:
                # Calculate number of samples for file2 at new sample rate
                num_samples = int(len(data2) * (sample_rate1 / sample_rate2))
                data2 = np.interp(
                    np.linspace(0, len(data2), num_samples),
                    np.arange(len(data2)),
                    data2
                )

            # Adjust lengths to match
            min_length = min(len(data1), len(data2))
            data1 = data1[:min_length]
            data2 = data2[:min_length]

            # Mix with volumes and normalize
            mixed_data = (data1 * volume1 + data2 * volume2)
            
            # Normalize to prevent clipping
            max_val = np.max(np.abs(mixed_data))
            if max_val > 0:
                mixed_data = mixed_data / max_val

            return mixed_data, sample_rate1

        except Exception as e:
            print(f"Error mixing audio: {e}")
            return None