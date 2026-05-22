import sounddevice as sd
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def capture_and_plot(duration=5, sr=22050):
    print(f"\n🔴 RECORDING STARTING... Speak or make noise for {duration} seconds!")
    
    # 1. Record live audio from your laptop mic
    # sounddevice records this as a raw mathematical matrix (NumPy array)
    audio_data = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()  # Wait until the 5 seconds are finished
    print("🛑 RECORDING STOPPED. Processing sound patterns...")
    
    # 2. Flatten the matrix to a 1D array for Librosa
    y = audio_data.flatten()
    
    # 3. Convert the raw audio mathematical array into a Mel Spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    # 4. Plot the visual sound signature
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title("Live Audio Visual Signature (Spectrogram)")
    plt.tight_layout()
    print("📊 Opening graph window...")
    plt.show()

# Run the live engine
capture_and_plot()