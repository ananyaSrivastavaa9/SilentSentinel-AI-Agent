import pandas as pd
import sounddevice as sd
import numpy as np
import librosa
import joblib
import time

SR = 22050
DURATION = 2  # Read the room in 2-second windows

print("🧠 Loading your AI sentinel brain...")
# 1. Load the trained machine learning model
try:
    model = joblib.load('sentinel_brain.pkl')
    print("💾 Brain loaded successfully!")
except:
    print("❌ Could not find 'sentinel_brain.pkl'. Please run train_ai.py first.")
    exit()

def extract_live_features(audio_data):
    y = audio_data.flatten()
    mfccs = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=13)
    avg_mfccs = np.mean(mfccs.T, axis=0).reshape(1, -1)
    
    # Wrap it in a DataFrame with the exact column names used during training
    feature_names = [f"mfcc_{i}" for i in range(13)]
    return pd.DataFrame(avg_mfccs, columns=feature_names)

print("\n🛡️ SILENT SENTINEL IS ACTIVE AND LISTENING... (Press Ctrl+C to stop)")

try:
    while True:
        # 2. Record a continuous 2-second block of sound
        audio_data = sd.rec(int(DURATION * SR), samplerate=SR, channels=1, dtype='float32')
        sd.wait()
        
        # 3. Process the sound block into its 13-number fingerprint
        features = extract_live_features(audio_data)
        
        # 4. Ask the AI to predict what it heard
        prediction = model.predict(features)[0]
        
        # 5. Output the result
        if prediction == "alert":
            print(f"⚠️ [{time.strftime('%H:%M:%S')}] AI Status: ALERT DETECTED! (Clap/Scream pattern found)")
        else:
            print(f"🟢 [{time.strftime('%H:%M:%S')}] AI Status: Normal background audio.")
            
except KeyboardInterrupt:
    print("\n🛑 Sentinel deactivated safely.")