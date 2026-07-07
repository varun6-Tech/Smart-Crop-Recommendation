# Smart Crop Recommendation and Fertilizer Suggestion System

This project is a Deep Learning-based web application that helps farmers identify the most suitable crop based on soil nutrients (Nitrogen, Phosphorus, Potassium, pH) and environmental conditions (Temperature, Humidity, Rainfall). It also provides fertilizer recommendations, water requirements, sowing seasons, and farming tips.

## Technologies Used
- **Python**
- **TensorFlow/Keras** (Artificial Neural Network)
- **Streamlit** (Web Application Framework)
- **Scikit-learn**, **Pandas**, **NumPy**, **Joblib**

## Features
- **Crop Recommendation:** Predicts the best crop to plant based on 7 input features.
- **Fertilizer Suggestion:** Suggests appropriate fertilizers for the predicted crop.
- **Farming Guidance:** Provides water requirements, best sowing season, and extra farming tips.
- **Modern Dashboard:** A green-themed UI for a professional, farmer-friendly experience.

## Project Structure
```text
SmartCropRecommendation/
├── app.py                     # Streamlit web application
├── train_model.py             # Script to train the Deep Learning model
├── utils.py                   # Helper functions mapping crops to fertilizers/tips
├── requirements.txt           # Python dependencies
├── dataset/
│   └── Crop_recommendation.csv # Training data
├── model/                     # Directory where the trained model is saved
│   ├── crop_model.keras
│   ├── label_encoder.pkl
│   └── scaler.pkl
└── assets/                    # Image assets (logos, banners)
```

## Setup and Installation

1. **Clone the repository or download the source code.**
2. **Navigate to the project directory:**
   ```bash
   cd SmartCropRecommendation
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Train the Deep Learning Model:**
   Before running the app, train the ANN model to generate the `.keras` and `.pkl` files.
   ```bash
   python train_model.py
   ```
5. **Run the Application:**
   You can launch the dashboard using one of the following methods:
   - **Option 1 (Recommended):** Simply double-click `Start_Project.bat` in the project root folder.
   - **Option 2:** Run manually via the terminal:
     ```bash
     cd <project_folder>
     streamlit run app.py
     ```

## Screenshots
*(Add screenshots of your working Streamlit application here)*
