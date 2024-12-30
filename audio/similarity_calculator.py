import numpy as np

class SimilarityCalculator:
    def __init__(self):
        self.weights = {
            'full': {'mfcc': 0.4, 'spectral': 0.3, 'chroma': 0.2, 'tempo': 0.1},
            'vocals': {'mfcc': 0.5, 'spectral': 0.3, 'chroma': 0.1, 'tempo': 0.1},
            'music': {'mfcc': 0.2, 'spectral': 0.3, 'chroma': 0.3, 'tempo': 0.2}
        }

    def normalize_array(self, arr):
        arr = np.array(arr)
        min_val = np.min(arr)
        max_val = np.max(arr)
        if max_val == min_val:
            return np.zeros_like(arr)
        return (arr - min_val) / (max_val - min_val)

    def normalize_value(self, val):
        return float(val) / (1 + abs(float(val)))

    def calculate_similarity(self, features1, features2, file_type='full'):
        mfcc_diff = np.sqrt(np.mean(np.square(
            self.normalize_array(features1['mfcc_mean']) - 
            self.normalize_array(features2['mfcc_mean'])
        )))
        
        spectral_diff = abs(
            self.normalize_value(features1['spectral_centroid_mean']) - 
            self.normalize_value(features2['spectral_centroid_mean'])
        )
        
        chroma_diff = np.sqrt(np.mean(np.square(
            self.normalize_array(features1['chroma_mean']) - 
            self.normalize_array(features2['chroma_mean'])
        )))
        
        tempo_diff = abs(features1['tempo'] - features2['tempo']) / max(features1['tempo'], 1)

        weights = self.weights[file_type]
        total_diff = (
            weights['mfcc'] * mfcc_diff +
            weights['spectral'] * spectral_diff +
            weights['chroma'] * chroma_diff +
            weights['tempo'] * tempo_diff
        )

        similarity = 100 * (1 - min(total_diff, 1))
        return max(0, min(100, similarity))