import sounddevice as sd
import numpy as np
import librosa
import time

SAMPLE_RATE = 22050     # Standard audio processing sample rate
BLOCK_SIZE = 22050      # 1 full second of audio per processing window
ENERGY_THRESHOLD = 0.05 # Minimum volume to wake up processing
STRESS_THRESHOLD = 2500 # Frequencies (in Hz) above this indicate high-pitched stress/screams

# This global variable acts as the inter-module signal link for our Agent
CRITICAL_PANIC_FLAG = False

print("🛡️ [SILENT SENTINEL] Acoustic Security Layer initializing...")

def analyze_acoustic_frame(indata, frames, time_info, status):
    global CRITICAL_PANIC_FLAG
    if status:
        print(f"⚠️ Audio Status Warning: {status}")
        
    # Flatten the raw microphone incoming matrix to a 1D array
    audio_frame = indata.flatten()
    
    # Calculate Root Mean Square (RMS) to check raw loudness/energy
    rms = np.sqrt(np.mean(audio_frame**2))
    
    # Optimization: If the room is quiet, skip heavy mathematical computations
    if rms < ENERGY_THRESHOLD:
        print(f"🟢 Monitoring... Room Ambient Level: {rms:.4f}", end="\r")
        return

    # Calculate Spectral Centroid (The visual "center of mass" of the sound frequencies)
    # Screams and whistles have a significantly higher spectral centroid than talking
    spectral_centroids = librosa.feature.spectral_centroid(y=audio_frame, sr=SAMPLE_RATE)
    mean_centroid = np.mean(spectral_centroids)
    
    # Clear line printing for debugging inside the VS Code terminal
    print(f"🔊 Sound Detected! Energy: {rms:.4f} | Center Pitch: {mean_centroid:.2f} Hz")
    
    # --- CRISIS REASONING LOGIC ---
    # Trigger condition: Sound is loud AND the pitch signature breaks into the scream barrier
    if mean_centroid > STRESS_THRESHOLD:
        CRITICAL_PANIC_FLAG = True
        print(f"\n🚨 [CRITICAL ACOUSTIC TRIGGER] High-Stress Audio Signature Identified!")
        print(f"↳ Verification Metric: Centroid {mean_centroid:.2f} Hz exceeded Threshold {STRESS_THRESHOLD} Hz.")
        print(f"⚡ Global Panic Status: {CRITICAL_PANIC_FLAG} -> Initiating Countdown Core...")
        print("---------------------------------------------------------------------")

# --- MICROPHONE STREAM INGESTION ---
print("🎙️ Microphone stream linked successfully. Listening for anomalies...")
try:
    with sd.InputStream(
        callback=analyze_acoustic_frame, 
        channels=1, 
        samplerate=SAMPLE_RATE, 
        blocksize=BLOCK_SIZE
    ):
        while not CRITICAL_PANIC_FLAG:
            # Keep the main execution thread alive while the audio background thread listens
            time.sleep(0.1)
            
        # Stopping loop once flag flips so we can pass control to the future countdown/Foundry module
        print("\n[SYSTEM NOTE] Acoustic module safely locked in PANIC state. Handing over processing pipeline.")

except KeyboardInterrupt:
    print("\n🛑 Acoustic security core closed safely by user.")