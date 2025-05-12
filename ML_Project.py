import streamlit as st
import base64
import os

# Function to encode the image file to base64 for embedding it
def get_base64_of_image(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Decision tree logic implemented manually
def decision_tree_predict(marks, attendance, assignments, extra):
    if marks >= 40:
        if attendance >= 75:
            if assignments >= 50:
                return "Pass"
            elif extra >= 60:
                return "Pass"
            else:
                return "Fail"
        else:
            if extra >= 70:
                return "Pass"
            else:
                return "Fail"
    else:
        return "Fail"

# Streamlit UI Configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered"
)

# Local background image handling
try:
    image_path = "image.png"  # Make sure this matches your actual image filename
    background_image = get_base64_of_image(image_path)
except FileNotFoundError:
    st.error("Background image not found! Please check the image file.")
    background_image = None

# Page styling with enhanced visibility
st.markdown(f"""
    <style>
        /* Full-page background */
        .stApp {{
            background-image: url('data:image/png;base64,{background_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            min-height: 100vh;
        }}

        /* Text styling */
        h1, h2, h3, h4, h5, h6, .stMarkdown {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }}

        /* Input field styling */
        .stNumberInput label, .stNumberInput input {{
            color: white !important;
        }}
        .stNumberInput input {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: #333 !important;
            border-radius: 8px;
        }}

        /* Button styling */
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

        /* Prediction result styling */
        .prediction {{
            font-size: 1.4rem;
            font-weight: bold;
            text-align: center;
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.15);
        }}

        /* Remove container padding */
        .stContainer {{
            padding: 0 !important;
        }}
    </style>
""", unsafe_allow_html=True)

# Main content
st.title("Student Performance Predictor 🎓")
st.markdown("Predict student outcomes based on academic and extracurricular performance")

# Input fields for the form
col1, col2 = st.columns(2)
with col1:
    marks = st.number_input("Internal Assessment Marks (0-100)", 
                           min_value=0, max_value=100, value=70)
    attendance = st.number_input("Attendance % (0-100)", 
                                min_value=0, max_value=100, value=80)
with col2:
    assignments = st.number_input("Assignment Score (0-100)", 
                                 min_value=0, max_value=100, value=60)
    extra = st.number_input("Extracurricular Participation Score (0-100)", 
                           min_value=0, max_value=100, value=50)

# Prediction logic
if st.button("📊 Get Prediction"):
    if all([val is not None for val in [marks, attendance, assignments, extra]]):
        result = decision_tree_predict(marks, attendance, assignments, extra)
        result_color = "#28a745" if result == "Pass" else "#dc3545"
        st.markdown(f'<div class="prediction" style="color: {result_color}">Prediction: {result}</div>', 
                    unsafe_allow_html=True)
    else:
        st.warning("Please fill in all fields before predicting.")