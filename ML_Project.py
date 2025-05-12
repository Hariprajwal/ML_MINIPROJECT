import streamlit as st
import base64

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

# Streamlit UI
st.title("Student Performance Predictor")

# Input fields for the form
marks = st.number_input("Internal Assessment Marks (0-100)", min_value=0, max_value=100)
attendance = st.number_input("Attendance % (0-100)", min_value=0, max_value=100)
assignments = st.number_input("Assignment Score (0-100)", min_value=0, max_value=100)
extra = st.number_input("Extracurricular Participation Score (0-100)", min_value=0, max_value=100)

# Prediction logic
if st.button("Predict"):
    if marks is not None and attendance is not None and assignments is not None and extra is not None:
        result = decision_tree_predict(marks, attendance, assignments, extra)
        st.write(f"**Prediction: {result}**")
    else:
        st.write("Please enter all values.")

# Local background image
image_path = "background.jpg"  # Replace with the path to your local image file
background_image = get_base64_of_image(image_path)

# Styling (Including local background image)
st.markdown(f"""
    <style>
        .css-1d391kg {{
            font-family: 'Segoe UI', sans-serif;
            background-color: #f0f4f8;
            padding: 40px;
            background-image: url('data:image/jpeg;base64,{background_image}');
            background-size: cover;
            background-position: center;
            height: 100vh;
            color: white;
        }}
        .stButton > button {{
            background-color: #007bff;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
        }}
        .stButton > button:hover {{
            background-color: #0056b3;
        }}
        .stTitle {{
            color: white;
        }}
        .stMarkdown {{
            color: white;
        }}
    </style>
""", unsafe_allow_html=True)
