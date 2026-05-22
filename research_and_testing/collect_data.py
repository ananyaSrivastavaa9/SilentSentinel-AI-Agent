import sounddevice as sd
import numpy as np
import librosa
import csv
import time

SR = 22050
DURATION = 2  # Collect sound in 2-second bursts

def extract_features(audio_data):
    # Flatten the raw audio array
    y = audio_data.flatten()
    # Extract 13 MFCC features (the standard "fingerprint" count for audio ML)
    mfccs = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=13)
    # Take the mathematical average over time so we get exactly 13 numbers
    return np.mean(mfccs.T, axis=0)

def gather_samples(label_name, total_samples=10):
    print(f"\n--- Preparing to collect data for: {label_name.upper()} ---")
    print("Get ready. We will capture 10 samples. Each sample takes 2 seconds.")
    time.sleep(2)
    
    features_list = []
    
    for i in range(total_samples):
        print(f"\n🎤 [Recording Sample {i+1}/{total_samples}] Start making sound NOW...")
        audio_data = sd.rec(int(DURATION * SR), samplerate=SR, channels=1, dtype='float32')
        sd.wait()
        print("🛑 Stopped recording. Processing...")
        
        # Turn sound into a list of 13 numbers
        features = extract_features(audio_data)
        
        # Append the label (0 for normal, 1 for alert) so the AI knows what it's looking at
        row = list(features) + [label_name]
        features_list = [] # clear out for saving
        
        # Save straight to a CSV file (our dataset!)
        with open('audio_dataset.csv', mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            
    print(f"✅ Finished collecting all {total_samples} samples for {label_name}!")

# Let's initialize the dataset file with headers
with open('audio_dataset.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    # 13 MFCC features columns + 1 target Label column
    headers = [f"mfcc_{i}" for i in range(13)] + ["label"]
    writer.writerow(headers)

# RUNNING DATA COLLECTION
# 1. Collect Normal Data
gather_samples("normal", total_samples=10)

print("\nTake a 5-second breath. Next, we will collect ALERT sounds (claps/screams).")
time.sleep(5)

# 2. Collect Alert Data
gather_samples("alert", total_samples=10)