import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def evaluate_pipeline():
    print("Loading models...")
    model_path = os.path.join(BASE_DIR, 'model', 'crop_model.keras')
    scaler_path = os.path.join(BASE_DIR, 'model', 'scaler.pkl')
    encoder_path = os.path.join(BASE_DIR, 'model', 'label_encoder.pkl')
    
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
    
    print("Loading dataset...")
    csv_path = os.path.join(BASE_DIR, "dataset", "Crop_recommendation.csv")
    df = pd.read_csv(csv_path)
    
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Randomly select 10 samples
    sample_df = df.sample(10, random_state=42)
    
    print("\n--- 10 Sample Predictions ---")
    for idx, row in sample_df.iterrows():
        # Prepare inference format identical to app.py
        input_df = pd.DataFrame([row[feature_cols].values], columns=feature_cols).astype(np.float32)
        scaled_input = scaler.transform(input_df)
        probs = model.predict(scaled_input, verbose=0)
        
        predicted_class_idx = int(np.argmax(probs, axis=1)[0])
        predicted_crop = label_encoder.inverse_transform([predicted_class_idx])[0]
        confidence = float(np.max(probs))
        
        print(f"Features: {row[feature_cols].to_dict()}")
        print(f"Actual: {row['label']}")
        print(f"Predicted: {predicted_crop}")
        print(f"Confidence: {confidence:.2f}\n")
        
    print("--- Full Dataset Evaluation ---")
    X_full = df[feature_cols].astype(np.float32)
    y_full = df['label']
    
    X_scaled = scaler.transform(X_full)
    probs_full = model.predict(X_scaled, verbose=0)
    y_pred_idx = np.argmax(probs_full, axis=1)
    y_pred = label_encoder.inverse_transform(y_pred_idx)
    
    print("\nClassification Report:")
    print(classification_report(y_full, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_full, y_pred))

if __name__ == '__main__':
    evaluate_pipeline()
