import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def train_and_save_model():
    print("Loading dataset...")
    csv_path = os.path.join(BASE_DIR, "dataset", "Crop_recommendation.csv")
    df = pd.read_csv(csv_path)
    
    # 1. Ensure exact data preprocessing order and cast to float32
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[feature_cols].astype(np.float32)
    y = df['label']
    
    # 2. Label encoding MUST happen BEFORE model training
    print("Encoding labels...")
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    num_classes = len(label_encoder.classes_)
    
    # Split data FIRST before scaling to avoid data leakage
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # 3. Scaling rules: fit_transform ONLY on training data
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Number of classes: {num_classes}")
    
    # 4. Model training (softmax output matches label classes)
    print("Building Deep Learning Model (ANN) with scikit-learn...")
    model = MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', max_iter=100, random_state=42, verbose=True)
    
    print("Training model...")
    model.fit(X_train_scaled, y_train)
    
    print("Evaluating model...")
    accuracy = model.score(X_test_scaled, y_test)
    print(f"Test Accuracy: {accuracy*100:.2f}%")
    
    # 5. SAVE ARTIFACTS IN SAME RUN (MANDATORY)
    print("Saving synchronized artifacts...")
    model_dir = os.path.join(BASE_DIR, 'model')
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, 'crop_model.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(label_encoder, os.path.join(model_dir, 'label_encoder.pkl'))
    print("Training complete. Assets saved in 'model/' directory.")

if __name__ == "__main__":
    train_and_save_model()
