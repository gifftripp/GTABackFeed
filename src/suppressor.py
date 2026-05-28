import noisereduce as nr
import soundfile as sf
import numpy as np

class AudioSuppressor:
    def reduce_noise(self, input_path: str, output_path: str, reduction_strength: float = 0.7):
        # Load audio file
        data, rate = sf.read(input_path)
        
        # Apply noise reduction
        reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=reduction_strength)
        
        # Save output
        sf.write(output_path, reduced_noise, rate)
        print(f'Noise reduction complete. Saved to {output_path}')
