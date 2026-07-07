import streamlit as st
import sys
import re
import os
import numpy as np
import joblib
import pandas as pd
import base64
from pathlib import Path
from fpdf import FPDF
import datetime
from utils import get_crop_details, get_fertilizer_details



BASE_DIR = Path(__file__).resolve().parent

# Configuration
st.set_page_config(
    page_title="Smart Crop & Fertilizer System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_ml_models():
    model_path = BASE_DIR / 'model' / 'crop_model.pkl'
    scaler_path = BASE_DIR / 'model' / 'scaler.pkl'
    encoder_path = BASE_DIR / 'model' / 'label_encoder.pkl'
    
    # 2. Print paths
    print("\n--- DEPLOYMENT DIAGNOSTICS ---")
    print(f"Model path: {model_path}")
    print(f"Scaler path: {scaler_path}")
    print(f"Encoder path: {encoder_path}")
    
    # 3. Print cwd and project dir
    print(f"Current Working Directory (os.getcwd()): {os.getcwd()}")
    print(f"Absolute Project Directory (BASE_DIR): {BASE_DIR}")
    
    # 4. Recursively list every file and folder
    print("--- DIRECTORY TREE ---")
    for root, dirs, files in os.walk(BASE_DIR):
        if '__pycache__' in root or '.git' in root or 'venv' in root:
            continue
        level = root.replace(str(BASE_DIR), '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")
    print("------------------------------\n")
    
    # 8. Compare filenames case-sensitively
    model_dir = BASE_DIR / 'model'
    if model_dir.exists():
        actual_files = os.listdir(model_dir)
        expected_files = ['crop_model.pkl', 'scaler.pkl', 'label_encoder.pkl']
        for exp in expected_files:
            if exp not in actual_files:
                for act in actual_files:
                    if act.lower() == exp.lower():
                        st.error(f"🚨 Case-Sensitive Mismatch Detected! Expected `{exp}` but found `{act}` in repository.")
                        st.stop()
    
    missing_files = []
    if not model_path.exists():
        missing_files.append(f"crop_model.pkl")
    if not scaler_path.exists():
        missing_files.append(f"scaler.pkl")
    if not encoder_path.exists():
        missing_files.append(f"label_encoder.pkl")
        
    if missing_files:
        st.warning(f"🚨 Missing Required Model Files: {', '.join(missing_files)}. Auto-healing by regenerating models dynamically (this will take ~5 seconds)...")
        try:
            import train_model
            train_model.train_and_save_model()
            st.success("Models generated successfully!")
            
            if not model_path.exists():
                st.error("Failed to write to filesystem. Streamlit Cloud might be restricting writes. You MUST push the `.pkl` files to GitHub manually.")
                st.stop()
        except Exception as e:
            st.error("Failed to generate models dynamically.")
            import traceback
            st.code(traceback.format_exc())
            st.stop()
    
    # Catch any hidden FileNotFoundError during joblib internal ops
    import traceback
    try:
        model = joblib.load(str(model_path))
    except FileNotFoundError as e:
        st.error(f"🚨 FileNotFoundError inside joblib.load(model_path)!\nVariable passed: {model_path}\nExists before load? {model_path.exists()}")
        st.code(traceback.format_exc())
        st.stop()
        
    try:
        scaler = joblib.load(str(scaler_path))
    except FileNotFoundError as e:
        st.error(f"🚨 FileNotFoundError inside joblib.load(scaler_path)!\nVariable passed: {scaler_path}\nExists before load? {scaler_path.exists()}")
        st.code(traceback.format_exc())
        st.stop()
        
    try:
        label_encoder = joblib.load(str(encoder_path))
    except FileNotFoundError as e:
        st.error(f"🚨 FileNotFoundError inside joblib.load(encoder_path)!\nVariable passed: {encoder_path}\nExists before load? {encoder_path.exists()}")
        st.code(traceback.format_exc())
        st.stop()
    
    if scaler.n_features_in_ != 7:
        raise ValueError("Scaler feature mismatch")
    if len(label_encoder.classes_) == 0:
        raise ValueError("Encoder empty")
    if model.n_outputs_ != len(label_encoder.classes_):
        raise ValueError("Model output shape mismatch")
        
    return model, scaler, label_encoder

model, scaler, label_encoder = load_ml_models()

if model is None or scaler is None or label_encoder is None:
    st.error("Model artifacts are not synchronized. Please train the model first.")
    st.stop()

# State Management
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'
if 'history' not in st.session_state:
    st.session_state.history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

def toggle_theme():
    st.session_state.theme = 'Dark' if st.session_state.theme == 'Light' else 'Light'

def clear_history():
    st.session_state.history = []

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_logo(location=st, title="Agri Smart", font_size="24px", width="45px"):
    logo_path = os.path.join(BASE_DIR, 'assets', 'logo.png')
    if os.path.exists(logo_path):
        base64_logo = get_base64_of_bin_file(logo_path)
        img_html = f"<img src='data:image/png;base64,{base64_logo}' style='width: {width}; vertical-align: middle; margin-right: 12px;'>"
    else:
        img_html = "<span style='font-size: 32px; vertical-align: middle; margin-right: 12px;'>🌱</span>"
        
    html = f"""
    <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 20px;'>
        {img_html}
        <span style='font-size: {font_size}; font-weight: bold; font-family: sans-serif;'>{title}</span>
    </div>
    """
    location.markdown(html, unsafe_allow_html=True)

def add_to_history(pred_type, result, confidence=None, inputs=None):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.history.insert(0, {
        "time": now_str,
        "type": pred_type,
        "result": result,
        "confidence": confidence,
        "inputs": inputs or {}
    })
    st.session_state.history = st.session_state.history[:10]

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None

def generate_txt_report(report_data):
    txt = f"=== SMART AGRICULTURE AI : PROFESSIONAL REPORT ===\n"
    txt += f"Project: Smart Agriculture AI\n"
    txt += f"Version: 1.0\n"
    txt += f"Date & Time: {report_data['time']}\n"
    txt += f"User: {st.session_state.username}\n"
    txt += f"Prediction Type: {report_data['type']}\n"
    txt += f"\n--- INPUT PARAMETERS ---\n"
    for k, v in report_data.get('inputs', {}).items():
        txt += f"{k}: {v}\n"
    txt += f"\n--- PREDICTION RESULT ---\n"
    txt += f"Result: {report_data['result']}\n"
    if report_data.get('confidence'):
        txt += f"Confidence Score: {report_data['confidence']:.1f}%\n"
        
    txt += f"\n--- DETAILED INFORMATION ---\n"
    if 'Crop' in report_data['type']:
        details = get_crop_details(report_data['result'])
        txt += f"Suitable Season: {details.get('season', 'N/A')}\n"
        txt += f"Suitable Soil Type: {details.get('soil_type', 'N/A')}\n"
        txt += f"Water Requirement: {details.get('water_req', 'N/A')}\n"
        txt += f"Growth Duration: {details.get('growth_duration', 'N/A')}\n"
        txt += f"Average Yield: {details.get('avg_yield', 'N/A')}\n"
        txt += f"Description: {details.get('description', 'N/A')}\n"
        txt += f"Farming Practices: {details.get('farming_practices', 'N/A')}\n"
    else:
        details = get_fertilizer_details(report_data['result'])
        txt += f"Application Method: {details.get('application_method', 'N/A')}\n"
        txt += f"Recommended Quantity: {details.get('recommended_quantity', 'N/A')}\n"
        txt += f"Best Time to Apply: {details.get('best_time', 'N/A')}\n"
        txt += f"Benefits: {details.get('benefits', 'N/A')}\n"
        txt += f"Precautions: {details.get('precautions', 'N/A')}\n"
        
    txt += "\nThank you for using Smart Agriculture AI.\n"
    return txt.encode('utf-8')

def generate_pdf_report(report_data):
    def clean_text(text):
        if not isinstance(text, str):
            text = str(text)
        text = text.replace('•', '-')
        text = text.replace('✔', 'Success')
        text = text.replace('✖', 'Error')
        text = text.replace('✓', 'Yes')
        text = text.replace('✗', 'No')
        text = re.sub(r'[𐀀-]', '', text)
        text = re.sub(r'[☀-➿]', '', text)
        return text.encode('ascii', 'ignore').decode('ascii')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    logo_path = os.path.join(BASE_DIR, 'assets', 'logo.png')
    if os.path.exists(logo_path):
        try:
            pdf.image(logo_path, x=(pdf.w - 15) / 2, y=10, w=15)
        except RuntimeError:
            try:
                # The file might actually be a JPEG saved with a .png extension
                pdf.image(logo_path, x=(pdf.w - 15) / 2, y=10, w=15, type='JPG')
            except Exception:
                pass
        pdf.ln(15)
    
    # Calculate exact printable width to prevent FPDFException
    printable_width = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font("Arial", 'B', 18)
    pdf.cell(printable_width, 12, "AGRI SMART: PREDICTION REPORT", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(printable_width, 6, "AI-Powered Crop & Fertilizer System | Version 1.0", ln=True, align='C')
    pdf.ln(8)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(printable_width, 8, "SESSION DETAILS", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(printable_width, 6, clean_text(f"Date & Time: {report_data['time']}"), ln=True)
    pdf.cell(printable_width, 6, clean_text(f"User: {st.session_state.username}"), ln=True)
    pdf.cell(printable_width, 6, clean_text(f"Prediction Type: {report_data['type']}"), ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(printable_width, 8, "INPUT PARAMETERS", ln=True)
    pdf.set_font("Arial", '', 11)
    for k, v in report_data.get('inputs', {}).items():
        pdf.cell(printable_width, 6, clean_text(f"  - {k}: {v}"), ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(printable_width, 8, "PREDICTION RESULT", ln=True)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(printable_width, 6, clean_text(f"  Result: {report_data['result']}"), ln=True)
    if report_data.get('confidence'):
        pdf.cell(printable_width, 6, clean_text(f"  Confidence: {report_data['confidence']:.1f}%"), ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(printable_width, 8, "DETAILED INFORMATION", ln=True)
    pdf.set_font("Arial", '', 11)
    
    def write_detail(k, v):
        if not v or str(v).strip() == "":
            v = "N/A"
        
        # Reset X to left margin before and after writing to prevent out-of-bounds error
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(printable_width, 6, clean_text(f"{k}: {v}"))
        pdf.set_x(pdf.l_margin)

    if 'Crop' in report_data['type']:
        details = get_crop_details(report_data['result'])
        for k, v in {
            "Season": details.get('season', ''),
            "Soil Type": details.get('soil_type', ''),
            "Water Req": details.get('water_req', ''),
            "Duration": details.get('growth_duration', ''),
            "Yield": details.get('avg_yield', ''),
            "Practices": details.get('farming_practices', '')
        }.items():
            write_detail(k, v)
    else:
        details = get_fertilizer_details(report_data['result'])
        for k, v in {
            "Method": details.get('application_method', ''),
            "Quantity": details.get('recommended_quantity', ''),
            "Best Time": details.get('best_time', ''),
            "Benefits": details.get('benefits', ''),
            "Precautions": details.get('precautions', '')
        }.items():
            write_detail(k, v)
            
    output = pdf.output(dest='S')
    if isinstance(output, str):
        return output.encode('latin-1')
    return bytes(output)

# Authentication Guard
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.write("")
        st.write("")
        st.write("")
        with st.container(border=True):
            render_logo(st, title="Agri Smart", font_size="28px", width="50px")
            st.caption("AI-Powered Crop Recommendation & Fertilizer Suggestion System")
            
            with st.form("login_form", border=False):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if username and password:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Please enter both username and password")
    st.stop()

# Sidebar Navigation
render_logo(st.sidebar, title="Agri Smart", font_size="22px", width="45px")

if "nav_radio" not in st.session_state:
    st.session_state.nav_radio = "🏠 Home"

page = st.sidebar.radio("Navigation", ["🏠 Home", "🌾 Crop Recommendation", "🧪 Fertilizer Suggestion", "💡 Farming Tips", "ℹ️ About Project"], key="nav_radio")
# Theme toggle (Native mode switches rely on user settings, but we keep the button for compatibility)
# st.sidebar.button("🌓 Toggle Light/Dark Mode", on_click=toggle_theme, use_container_width=True)

st.sidebar.divider()
st.sidebar.subheader("📜 Prediction History")
if len(st.session_state.history) == 0:
    st.sidebar.info("No recent predictions.")
else:
    def load_history(h):
        st.session_state.active_report = h
        
    for i, h in enumerate(st.session_state.history):
        with st.sidebar.container(border=True):
            col_h1, col_h2 = st.columns([3, 1])
            with col_h1:
                st.caption(f"{h['time']}")
                st.write(f"**{h['type']}**")
                st.write(f"{h['result']}")
            with col_h2:
                st.button("👁️", key=f"hist_{i}", on_click=load_history, args=(h,), help="View Details")
            
    st.sidebar.button("🗑️ Clear History", on_click=clear_history, use_container_width=True)

st.sidebar.divider()
st.sidebar.subheader("ℹ️ About Project")
st.sidebar.caption("Smart Agriculture AI leverages advanced Deep Learning to provide optimal crop and fertilizer recommendations based on real-time soil and climatic data.")
st.sidebar.write("")
st.sidebar.button("🚪 Logout", on_click=logout, use_container_width=True)


if page == "🏠 Home":
    render_logo(st, title="Welcome to Agri Smart", font_size="36px", width="60px")
    st.subheader("Empowering farmers with intelligent, data-driven decisions for better yield and profit.")
    st.divider()
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.container(border=True):
            st.header("🌾")
            st.subheader("Crop Recommendation")
            st.write("Discover the most profitable crop to plant based on your specific NPK, pH, temperature, humidity, and rainfall.")
            
        with st.container(border=True):
            st.header("💡")
            st.subheader("Farming Tips")
            st.write("Gain valuable insights on the optimal sowing season, water requirements, and harvesting timelines for your crop.")
            
    with col2:
        with st.container(border=True):
            st.header("🧪")
            st.subheader("Fertilizer Suggestion")
            st.write("Receive tailored fertilizer recommendations designed specifically to bridge the nutrient gap in your current soil profile.")
            
        with st.container(border=True):
            st.header("🤖")
            st.subheader("AI Powered Prediction")
            st.write("Our Deep Learning models provide highly accurate predictions with real-time confidence scores to guide your decisions.")
            
    st.write("")
    
    def navigate_to_crop():
        st.session_state.nav_radio = "🌾 Crop Recommendation"
        
    st.button("🚀 Start", type="primary", use_container_width=True, on_click=navigate_to_crop)

elif page == "🌾 Crop Recommendation":
    st.title("Smart Crop Recommendation")
    st.subheader("Find the most optimal crop to plant based on your specific soil and environmental conditions.")
    st.divider()
    
    @st.fragment
    def render_crop_dashboard():
        if 'active_report' in st.session_state and st.session_state.active_report:
            if 'Crop' not in st.session_state.active_report['type']:
                st.session_state.active_report = None
        
        st.subheader("📊 Enter Soil & Environmental Parameters")
        with st.form(key="crop_prediction_form", border=True):
            grid_r1_c1, grid_r1_c2, grid_r1_c3 = st.columns(3)
            with grid_r1_c1: n = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=90, key="c_n", help="Enter Nitrogen value")
            with grid_r1_c2: p = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=42, key="c_p", help="Enter Phosphorus value")
            with grid_r1_c3: k = st.number_input("Potassium (K)", min_value=0, max_value=200, value=43, key="c_k", help="Enter Potassium value")
            
            grid_r2_c1, grid_r2_c2, grid_r2_c3 = st.columns(3)
            with grid_r2_c1: temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=20.8, key="c_t", help="Enter Temperature in Celsius")
            with grid_r2_c2: humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=82.0, key="c_h", help="Enter Humidity Percentage")
            with grid_r2_c3: ph = st.number_input("Soil pH (0–14)", min_value=0.0, max_value=14.0, value=6.5, key="c_ph", help="Enter Soil pH (0–14)")
            
            rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=202.9, key="c_r", help="Enter Rainfall in millimeters")
            predict_clicked = st.form_submit_button("Predict Crop", use_container_width=True)
            
        if predict_clicked or ('active_report' in st.session_state and st.session_state.active_report):
            if predict_clicked:
                st.session_state.active_report = None
                with st.spinner("Analyzing soil for optimal crop..."):
                    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                    features_df = pd.DataFrame([[n, p, k, temp, humidity, ph, rainfall]], columns=feature_cols).astype(np.float32)
                    features_scaled = scaler.transform(features_df)
                    crop_prediction_probs = model.predict_proba(features_scaled)
                    crop_predicted_class_idx = int(np.argmax(crop_prediction_probs, axis=1)[0])
                    confidence = np.max(crop_prediction_probs, axis=1)[0] * 100
                    crop_result = label_encoder.inverse_transform([crop_predicted_class_idx])[0].title()
                    
                    inputs_dict = {"Nitrogen (N)": n, "Phosphorus (P)": p, "Potassium (K)": k, "Temp (°C)": temp, "Humidity (%)": humidity, "Soil pH": ph, "Rainfall (mm)": rainfall}
                    add_to_history("Crop Rec.", crop_result, confidence, inputs=inputs_dict)
                    active = st.session_state.history[0]
            else:
                active = st.session_state.active_report
                crop_result = active['result']
                confidence = active['confidence']
                inputs_dict = active['inputs']
                
            details = get_crop_details(crop_result)
            
            st.divider()
            
            # Use Streamlit columns to center the result container, simulating max-width on desktop and full width on mobile
            _, center_col, _ = st.columns([1, 6, 1])
            
            with center_col:
                st.markdown("<h3 style='text-align: center;'>📊 Environmental Data Analysis</h3>", unsafe_allow_html=True)
                st.write("")
                with st.container(border=True):
                    v1, v2, v3 = st.columns(3)
                    v1.metric("Nitrogen (N)", f"{inputs_dict.get('Nitrogen (N)', 0)}", delta="Optimal" if 50 < inputs_dict.get('Nitrogen (N)', 0) < 120 else "Review")
                    v2.metric("Phosphorus (P)", f"{inputs_dict.get('Phosphorus (P)', 0)}", delta="Optimal" if 30 < inputs_dict.get('Phosphorus (P)', 0) < 80 else "Review")
                    v3.metric("Potassium (K)", f"{inputs_dict.get('Potassium (K)', 0)}", delta="Optimal" if 30 < inputs_dict.get('Potassium (K)', 0) < 80 else "Review")
                    
                    st.write("")
                    v4, v5, v6, v7 = st.columns(4)
                    v4.metric("pH Level", f"{inputs_dict.get('Soil pH', 0)}")
                    v5.metric("Temp", f"{inputs_dict.get('Temp (°C)', 0)}°C")
                    v6.metric("Humidity", f"{inputs_dict.get('Humidity (%)', 0)}%")
                    v7.metric("Rainfall", f"{inputs_dict.get('Rainfall (mm)', 0)}mm")
                
                st.write("")
                st.write("")
                
                st.markdown("<h3 style='text-align: center;'>🌱 Recommended Crop</h3>", unsafe_allow_html=True)
                st.write("")
                with st.container(border=True):
                    st.success(f"### ✔ {crop_result}")
                
                st.write("")
                st.write("")
                
                if confidence >= 90:
                    status = "Very High"
                elif confidence >= 75:
                    status = "High"
                elif confidence >= 50:
                    status = "Medium"
                else:
                    status = "Low"

                st.markdown("<h3 style='text-align: center;'>📈 Prediction Confidence</h3>", unsafe_allow_html=True)
                st.write("")
                with st.container(border=True):
                    st.metric("Confidence Score", f"{confidence:.1f}%", delta=status, delta_color="normal")
                    st.progress(int(confidence))
                
                st.write("")
                st.write("")
                
                st.markdown("<h3 style='text-align: center;'>💡 Recommendation</h3>", unsafe_allow_html=True)
                st.write("")
                with st.container(border=True):
                    st.info(f"Based on the provided soil and environmental metrics, **{crop_result}** is highly recommended for optimal yield.")
                    st.write(f"**Description:** {details.get('description', 'N/A')}")
                    
                    profile_df = pd.DataFrame({
                        "Attribute": ["Season", "Soil Type", "Water Req", "Duration", "Average Yield"],
                        "Value": [details.get('season', 'N/A'), details.get('soil_type', 'N/A'), details.get('water_req', 'N/A'), details.get('growth_duration', 'N/A'), details.get('avg_yield', 'N/A')]
                    })
                    st.table(profile_df)
                    st.write(f"**Best Practices:** {details.get('farming_practices', 'N/A')}")
                
                st.write("")
                st.write("")
                
                st.markdown("<h3 style='text-align: center;'>📥 Download Report</h3>", unsafe_allow_html=True)
                st.write("")
                dl_c1, dl_c2 = st.columns(2)
                with dl_c1:
                    st.download_button("Download TXT", data=generate_txt_report(active), file_name="crop_report.txt", use_container_width=True)
                with dl_c2:
                    st.download_button("Download PDF", data=generate_pdf_report(active), file_name="crop_report.pdf", mime="application/pdf", use_container_width=True)

        else:
            st.info("🔍 Enter the soil and environmental data in the left panel and click **Predict Crop** to see the analysis.")

    render_crop_dashboard()

elif page == "🧪 Fertilizer Suggestion":
    st.title("Fertilizer Suggestion System")
    @st.fragment
    def render_fert_dashboard():
        if 'active_report' in st.session_state and st.session_state.active_report:
            if 'Fertilizer' not in st.session_state.active_report['type']:
                st.session_state.active_report = None
                
        st.subheader("📊 Enter Soil & Crop Parameters")
        with st.form(key="fert_prediction_form", border=True):
            grid_r1_c1, grid_r1_c2, grid_r1_c3 = st.columns(3)
            with grid_r1_c1: n = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=90, key="f_n", help="Enter Nitrogen value")
            with grid_r1_c2: p = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=42, key="f_p", help="Enter Phosphorus value")
            with grid_r1_c3: k = st.number_input("Potassium (K)", min_value=0, max_value=200, value=43, key="f_k", help="Enter Potassium value")
            
            grid_r2_c1, grid_r2_c2, grid_r2_c3 = st.columns(3)
            with grid_r2_c1: temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=20.8, key="f_t", help="Enter Temperature in Celsius")
            with grid_r2_c2: humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=82.0, key="f_h", help="Enter Humidity Percentage")
            with grid_r2_c3: ph = st.number_input("Soil pH (0–14)", min_value=0.0, max_value=14.0, value=6.5, key="f_ph", help="Enter Soil pH (0–14)")
            
            rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=202.9, key="f_r", help="Enter Rainfall in millimeters")
            fert_clicked = st.form_submit_button("Suggest Fertilizer", use_container_width=True)
            
        if fert_clicked or ('active_report' in st.session_state and st.session_state.active_report):
            if fert_clicked:
                st.session_state.active_report = None
                with st.spinner("Analyzing nutrient gap..."):
                    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                    features_df = pd.DataFrame([[n, p, k, temp, humidity, ph, rainfall]], columns=feature_cols).astype(np.float32)
                    features_scaled = scaler.transform(features_df)
                    fert_prediction_probs = model.predict_proba(features_scaled)
                    fert_predicted_class_idx = int(np.argmax(fert_prediction_probs, axis=1)[0])
                    confidence = np.max(fert_prediction_probs, axis=1)[0] * 100
                    underlying_crop = label_encoder.inverse_transform([fert_predicted_class_idx])[0]
                    
                    crop_details = get_crop_details(underlying_crop)
                    fertilizer_result = crop_details['fertilizer']
                    
                    inputs_dict = {"Nitrogen (N)": n, "Phosphorus (P)": p, "Potassium (K)": k, "Temp (°C)": temp, "Humidity (%)": humidity, "Soil pH": ph, "Rainfall (mm)": rainfall}
                    add_to_history("Fertilizer", fertilizer_result, confidence, inputs=inputs_dict)
                    active = st.session_state.history[0]
            else:
                active = st.session_state.active_report
                fertilizer_result = active['result']
                confidence = active['confidence']
                inputs_dict = active['inputs']
                
            details = get_fertilizer_details(fertilizer_result)
            
            st.divider()
            
            # Use Streamlit columns to center the result container, simulating max-width on desktop and full width on mobile
            _, center_col, _ = st.columns([1, 6, 1])
            
            with center_col:
                st.markdown("<h3 style='text-align: center;'>📊 Soil Analysis Data</h3>", unsafe_allow_html=True)
                st.write("")
                with st.container(border=True):
                    v1, v2, v3 = st.columns(3)
                    v1.metric("Nitrogen (N)", f"{inputs_dict.get('Nitrogen (N)', 0)}", delta="Optimal" if 50 < inputs_dict.get('Nitrogen (N)', 0) < 120 else "Review")
                    v2.metric("Phosphorus (P)", f"{inputs_dict.get('Phosphorus (P)', 0)}", delta="Optimal" if 30 < inputs_dict.get('Phosphorus (P)', 0) < 80 else "Review")
                    v3.metric("Potassium (K)", f"{inputs_dict.get('Potassium (K)', 0)}", delta="Optimal" if 30 < inputs_dict.get('Potassium (K)', 0) < 80 else "Review")
                    
                    st.write("")
                    v4, v5, v6, v7 = st.columns(4)
                    v4.metric("pH Level", f"{inputs_dict.get('Soil pH', 0)}")
                    v5.metric("Temp", f"{inputs_dict.get('Temp (°C)', 0)}°C")
                    v6.metric("Humidity", f"{inputs_dict.get('Humidity (%)', 0)}%")
                    v7.metric("Rainfall", f"{inputs_dict.get('Rainfall (mm)', 0)}mm")
                
                st.write("")
                st.write("")
                
                st.markdown("<h3 style='text-align: center;'>🧪 Fertilizer Recommendation</h3>", unsafe_allow_html=True)
                st.write("")
                with st.container(border=True):
                    st.success(f"### ✔ {fertilizer_result}")
                
                st.write("")
                st.write("")
                
                if confidence >= 90:
                    status = "Very High"
                elif confidence >= 75:
                    status = "High"
                elif confidence >= 50:
                    status = "Medium"
                else:
                    status = "Low"

                st.markdown("<h3 style='text-align: center;'>📈 Prediction Confidence</h3>", unsafe_allow_html=True)
                st.write("")
                with st.container(border=True):
                    st.metric("Analysis Confidence", f"{confidence:.1f}%", delta=status, delta_color="normal")
                    st.progress(int(confidence))
                
                st.write("")
                st.write("")
                
                st.markdown("<h3 style='text-align: center;'>💡 Recommendation</h3>", unsafe_allow_html=True)
                st.write("")
                with st.container(border=True):
                    st.info(f"Based on the calculated nutrient gap, **{fertilizer_result}** is highly recommended to improve your soil profile.")
                    st.write(f"**Benefits:** {details.get('benefits', 'N/A')}")
                    
                    profile_df = pd.DataFrame({
                        "Attribute": ["Method", "Quantity", "Best Time"],
                        "Value": [details.get('application_method', 'N/A'), details.get('recommended_quantity', 'N/A'), details.get('best_time', 'N/A')]
                    })
                    st.table(profile_df)
                    st.write(f"**Precautions:** {details.get('precautions', 'N/A')}")
                
                st.write("")
                st.write("")
                
                st.markdown("<h3 style='text-align: center;'>📥 Download Report</h3>", unsafe_allow_html=True)
                st.write("")
                dl_c1, dl_c2 = st.columns(2)
                with dl_c1:
                    st.download_button("Download TXT", data=generate_txt_report(active), file_name="fert_report.txt", use_container_width=True)
                with dl_c2:
                    st.download_button("Download PDF", data=generate_pdf_report(active), file_name="fert_report.pdf", mime="application/pdf", use_container_width=True)
                    
        else:
            st.info("🔍 Enter the soil parameters in the left panel and click **Suggest Fertilizer** to see the analysis.")

    render_fert_dashboard()

elif page == "💡 Farming Tips":
    st.title("Farming Tips & Insights")
    st.subheader("Get actionable farming tips and seasonal data based on your environment.")
    st.divider()
    
    @st.fragment
    def render_tips_dashboard():
        st.subheader("📊 Enter Environmental Parameters")
        with st.form(key="tips_prediction_form", border=True):
            grid_r1_c1, grid_r1_c2, grid_r1_c3 = st.columns(3)
            with grid_r1_c1: n = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=90, key="t_n")
            with grid_r1_c2: p = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=42, key="t_p")
            with grid_r1_c3: k = st.number_input("Potassium (K)", min_value=0, max_value=200, value=43, key="t_k")
            
            grid_r2_c1, grid_r2_c2, grid_r2_c3 = st.columns(3)
            with grid_r2_c1: temp = st.number_input("Temp (°C)", min_value=0.0, max_value=60.0, value=20.8, key="t_t")
            with grid_r2_c2: humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=82.0, key="t_h")
            with grid_r2_c3: ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5, key="t_ph")
            
            rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=202.9, key="t_r")
            tips_clicked = st.form_submit_button("Get Tips", use_container_width=True)
            
        if tips_clicked:
            with st.spinner("Analyzing data for tips..."):
                feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                features_df = pd.DataFrame([[n, p, k, temp, humidity, ph, rainfall]], columns=feature_cols).astype(np.float32)
                features_scaled = scaler.transform(features_df)
                tips_prediction_probs = model.predict_proba(features_scaled)
                tips_predicted_class_idx = int(np.argmax(tips_prediction_probs, axis=1)[0])
                underlying_crop = label_encoder.inverse_transform([tips_predicted_class_idx])[0]
                
                tips_result = get_crop_details(underlying_crop)
                
                st.divider()
                
                _, center_col, _ = st.columns([1, 6, 1])
                
                with center_col:
                    st.markdown("<h3 style='text-align: center;'>💡 Farming Tips</h3>", unsafe_allow_html=True)
                    st.write("")
                    with st.container(border=True):
                        st.write(tips_result['tips'])
                        
                    st.write("")
                    st.write("")
                    
                    st.markdown("<h3 style='text-align: center;'>📋 Additional Info</h3>", unsafe_allow_html=True)
                    st.write("")
                    with st.container(border=True):
                        st.write(f"**Best Sowing Season:** {tips_result['season']}")
                        st.write(f"**Water Requirement:** {tips_result['water_req']}")
                        st.write(f"**Harvest Period:** {tips_result['harvest_period']}")
                        
        else:
            st.info("🔍 Enter the data above and click **Get Tips**.")

    render_tips_dashboard()

st.write("")
st.write("")
st.divider()
st.caption("© 2026 Smart Crop Recommendation System. All rights reserved. | Powered by TensorFlow and Streamlit")

if page == "ℹ️ About Project":
    st.title("About Smart Agriculture AI")
    st.subheader("Empowering the future of farming with Deep Learning and Data Science.")
    st.divider()
    
    with st.container(border=True):
        st.subheader("Project Description")
        st.write("Smart Agriculture AI is an enterprise-grade web application built to assist farmers in making data-driven decisions. By analyzing real-time soil metrics (Nitrogen, Phosphorus, Potassium, pH) and environmental conditions (Temperature, Humidity, Rainfall), the system accurately predicts the most profitable crop to plant and suggests the exact fertilizer required to bridge any nutrient gaps.")
        
        st.divider()
        
        st.subheader("Core Features")
        st.write("- **🌾 Crop Recommendation:** AI-driven analysis of 7 environmental parameters to recommend the best crop.")
        st.write("- **🧪 Fertilizer Suggestion:** Calculates soil nutrient gaps to suggest specific fertilizer application strategies.")
        st.write("- **📊 Data Visualization:** Interactive metric charts for immediate environment analysis.")
        st.write("- **📄 Professional Reporting:** Instantly generate downloadable PDF and TXT reports of predictions.")
        st.write("- **🔐 Session Security:** User authentication guard and session state retention.")
        
        st.divider()
        
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.subheader("Algorithms Used")
            st.write("- Deep Learning (TensorFlow/Keras)")
            st.write("- Feature Scaling (StandardScaler)")
            st.write("- Label Encoding (scikit-learn)")
        with col_a2:
            st.subheader("Technologies")
            st.write("- Python 3.10")
            st.write("- Streamlit (Web Framework)")
            st.write("- Pandas & NumPy")
            st.write("- FPDF2 (PDF Generation)")
        
        st.divider()
        
        st.caption("**Developer Information:** Designed for Final Year Engineering Project")
        st.caption("**Version:** 1.0.0-native")
