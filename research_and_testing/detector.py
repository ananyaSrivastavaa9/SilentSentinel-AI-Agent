import sounddevice as sd
import numpy as np

# This factor controls how sensitive our ear is. 
# If it's too sensitive, it triggers on normal talking. If too high, it misses claps.
THRESHOLD = 0.1  

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    
    # Calculate the Root Mean Square (RMS) energy of the current audio chunk
    # This turns thousands of sound waves into a single "loudness" number
    rms = np.sqrt(np.mean(indata**2))
    
    # Print a live volume meter in the terminal
    meter = "█" * int(rms * 100)
    print(f"Volume: {rms:.4f} {meter.ljust(50)}", end="\r")
    
    # Check if the volume crossed our safety threshold
    if rms > THRESHOLD:
        print(f"\n🚨 [CRITICAL ALERT] Sudden high energy detected! RMS: {rms:.4f}")

# Open a live, continuous stream from your microphone
# blocksize=2205 means it checks the room roughly 10 times every second
print("🎙️ Monitoring environment... Press Ctrl+C to stop.")
with sd.InputStream(callback=audio_callback, channels=1, samplerate=22050, blocksize=2205):
    while True:
        pass