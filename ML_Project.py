import streamlit as st
import base64
import os
import numpy as np

# Ensure joblib is imported properly
try:
    import joblib
except ImportError:
    st.error("joblib module not found. Please install it using `pip install joblib`.")
    raise

# Function to encode the image file to base64 for embedding it
def get_base64_of_image(image_file):
    try:
        with open(image_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        st.warning(f"Could not load background image: {e}")
        return None

# Load trained model and scaler
try:
    if hasattr(st, 'cache_resource'):  # Streamlit v1.18+
        @st.cache_resource
        def load_model_and_scaler(model_path, scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return model, scaler
    else:
        @st.cache(allow_output_mutation=True)
        def load_model_and_scaler(model_path, scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return model, scaler

    model, scaler = load_model_and_scaler('best_model.pkl', 'scaler.pkl')

except FileNotFoundError as e:
    st.error(f"Model or scaler file not found: {e}")
    st.stop()
except Exception as e:
    st.error(f"Failed to load model or scaler: {e}")
    st.stop()

# Streamlit UI Configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered"
)

# Local background image handling
background_image = None
image_path = "background.png"
if os.path.exists(image_path):
    background_image = get_base64_of_image(image_path)
else:
    st.warning(f"Background image not found: {image_path}")

# Page styling with enhanced visibility
if background_image:
    css = f"""
    <style>
        .stApp {{
            background-image: url('data:image/png;base64,{background_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            min-height: 100vh;
        }}
        h1, h2, h3, h4, h5, h6, .stMarkdown {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }}
        .stNumberInput label, .stNumberInput input {{
            color: white !important;
        }}
        .stNumberInput input {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: #333 !important;
            border-radius: 8px;
        }}
        .stButton > button {{
            background-color: #007bff !important;
            color: white !important;
            border-radius: 8px;
            padding: 10px 24px;
            transition: all 0.3s ease;
            border: none;
        }}
        .stButton > button:hover {{
            background-color: #0056b3 !important;
            transform: scale(1.05);
        }}
        .prediction {{
            font-size: 1.4rem;
            font-weight: bold;
            text-align: center;
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.15);
        }}
        .stContainer {{
            padding: 0 !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Main content
st.title("Student Performance Predictor 🎓")
st.markdown("Predict student outcomes based on academic and extracurricular performance")

# Input fields for the form
col1, col2 = st.columns(2)
with col1:
    marks = st.number_input(
        "Internal Assessment Marks (0-100)",
        min_value=0, max_value=100, value=70,
        key="marks"
    )
    attendance = st.number_input(
        "Attendance % (0-100)",
        min_value=0, max_value=100, value=80,
        key="attendance"
    )
with col2:
    assignments = st.number_input(
        "Assignment Score (0-100)",
        min_value=0, max_value=100, value=60,
        key="assignments"
    )
    extra = st.number_input(
        "Extracurricular Participation Score (0-100)",
        min_value=0, max_value=100, value=50,
        key="extra"
    )

# Prediction logic
def make_prediction():
    input_data = np.array([[marks, attendance, assignments, extra]])
    scaled_input = scaler.transform(input_data)
    pred = model.predict(scaled_input)[0]

    try:
        proba = model.predict_proba(scaled_input)[0][1]
        confidence = round(proba * 100, 1)
    except Exception:
        confidence = "N/A"

    label = "PASS ✅" if pred == 1 else "FAIL ❌"
    color = "#28a745" if pred == 1 else "#dc3545"
    return label, confidence, color

if st.button("🔮 Predict Performance"):
    try:
        if not all(0 <= x <= 100 for x in [marks, attendance, assignments, extra]):
            st.error("All values must be between 0 and 100.")
        else:
            result, confidence, color = make_prediction()
            st.markdown(
                f'<div class="prediction" style="color: {color}">'
                f'Prediction: {result} | Confidence: {confidence}%</div>',
                unsafe_allow_html=True
            )
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
