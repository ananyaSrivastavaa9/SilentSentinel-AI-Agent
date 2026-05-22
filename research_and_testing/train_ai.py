import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("🧠 Loading the sound fingerprint dataset...")
# 1. Read the CSV file you created
df = pd.read_csv('audio_dataset.csv')

# 2. Separate features (X = all 13 MFCC columns) from the target output (y = label)
X = df.drop(columns=['label'])
y = df['label']

# 3. Split the data into a training set (80%) and a testing set (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"📊 Training on {len(X_train)} samples, Testing on {len(X_test)} samples.")

# 4. Initialize our Random Forest AI model
model = RandomForestClassifier(n_estimators=50, random_state=42)

# 5. Train the AI! 
model.fit(X_train, y_train)

# 6. Evaluate how smart our AI is
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"🎯 AI Training complete! Model accuracy on test data: {accuracy * 100:.2f}%")

# 7. Save this trained brain to a file
joblib.dump(model, 'sentinel_brain.pkl')
print("💾 Saved the trained model as 'sentinel_brain.pkl'!")