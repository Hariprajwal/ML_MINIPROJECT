import streamlit as st
import base64
import os
import numpy as np

# Try to import joblib; fallback to pickle if unavailable
try:
    import joblib
except ImportError:
    import pickle as joblib
    st.warning("joblib not installed; using pickle as a fallback. Consider adding 'joblib' to your requirements.txt.")

# Function to encode an image file to base64 for embedding
def get_base64_of_image(image_file: str) -> str:
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Load trained model and scaler (cached for performance)
@st.cache_resource
def load_model_and_scaler(model_path: str, scaler_path: str):
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        st.error(f"Model or scaler file not found.\nExpected: {model_path}, {scaler_path}")
        st.stop()
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

# Paths to your artifacts
MODEL_PATH = 'best_model.pkl'
SCALER_PATH = 'scaler.pkl'

# Attempt to load the model and scaler
model, scaler = load_model_and_scaler(MODEL_PATH, SCALER_PATH)

# Page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered"
)

# Embed background image if available
image_path = "background.png"
if os.path.exists(image_path):
    try:
        bg_encoded = get_base64_of_image(image_path)
        css = f"""
        <style>
            .stApp {{
                background: url('data:image/png;base64,{bg_encoded}') no-repeat center/cover fixed;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception:
        st.warning("Could not load background image.")
else:
    st.info("No background image found. Continuing without it.")

# App title and description
st.title("Student Performance Predictor 🎓")
st.markdown("Predict student outcomes based on academic and extracurricular performance.")

# Input fields
col1, col2 = st.columns(2)
with col1:
    marks = st.number_input("Internal Assessment Marks (0–100)", 0, 100, 70)
    attendance = st.number_input("Attendance % (0–100)", 0, 100, 80)
with col2:
    assignments = st.number_input("Assignment Score (0–100)", 0, 100, 60)
    extra = st.number_input("Extracurricular Participation Score (0–100)", 0, 100, 50)

# Prediction logic
def make_prediction(marks, attendance, assignments, extra):
    data = np.array([[marks, attendance, assignments, extra]])
    scaled = scaler.transform(data)
    pred = model.predict(scaled)[0]
    proba = model.predict_proba(scaled)[0][1] * 100
    label = "PASS ✅" if pred == 1 else "FAIL ❌"
    color = "#28a745" if pred == 1 else "#dc3545"
    return label, round(proba, 1), color

if st.button("🔮 Predict Performance"):
    try:
        values = [marks, attendance, assignments, extra]
        if any(v < 0 or v > 100 for v in values):
            st.error("All input values must be between 0 and 100.")
        else:
            label, confidence, color = make_prediction(marks, attendance, assignments, extra)
            st.markdown(
                f"<div style='font-size:1.4rem;font-weight:bold;text-align:center;margin-top:1.5rem;padding:1rem;border-radius:8px;background:rgba(255,255,255,0.15);color:{color};'>"
                f"Prediction: {label} | Confidence: {confidence}%"
                "</div>", unsafe_allow_html=True
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")

# To run in Jupyter, first install dependencies:
# !pip install streamlit numpy scikit-learn joblib
# Then launch:
# !streamlit run path/to/this_script.py

# requirements.txt snippet (add to your repo):
# streamlit
# numpy
# scikit-learn
# joblib
