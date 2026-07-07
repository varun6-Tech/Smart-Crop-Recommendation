import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_evidence():
    print("\n--- REQUIREMENT 5: MODEL SUMMARY ---")
    model_path = os.path.join(BASE_DIR, 'model', 'crop_model.keras')
    model = tf.keras.models.load_model(model_path)
    model.summary()
    
    scaler_path = os.path.join(BASE_DIR, 'model', 'scaler.pkl')
    encoder_path = os.path.join(BASE_DIR, 'model', 'label_encoder.pkl')
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
    
    print("\n--- REQUIREMENT 6: ARTIFACT PROPERTIES ---")
    print(f"scaler.n_features_in_: {scaler.n_features_in_}")
    print(f"scaler.mean_: {scaler.mean_}")
    print(f"scaler.scale_: {scaler.scale_}")
    print(f"len(label_encoder.classes_): {len(label_encoder.classes_)}")
    print(f"model.output_shape: {model.output_shape}")
    
    print("\n--- REQUIREMENT 7: FIRST ROW PREDICTION ---")
    csv_path = os.path.join(BASE_DIR, "dataset", "Crop_recommendation.csv")
    df = pd.read_csv(csv_path)
    first_row = df.iloc[0]
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    raw_features = first_row[feature_cols].values
    actual_label = first_row['label']
    
    input_df = pd.DataFrame([raw_features], columns=feature_cols).astype(np.float32)
    scaled_features = scaler.transform(input_df)
    
    prob_vector = model.predict(scaled_features, verbose=0)[0]
    predicted_idx = int(np.argmax(prob_vector))
    predicted_label = label_encoder.inverse_transform([predicted_idx])[0]
    
    print(f"raw features: {raw_features}")
    print(f"scaled features: {scaled_features}")
    print(f"probability vector: {prob_vector}")
    print(f"predicted index: {predicted_idx}")
    print(f"predicted label: {predicted_label}")
    print(f"actual label: {actual_label}")

if __name__ == '__main__':
    extract_evidence()
