import streamlit as st
import requests
import json

# Set Page Configuration
st.set_page_config(page_title="Diabetes Progression Predictor", layout="centered")

st.title("🏥 Diabetes Progression Predictor")
st.markdown("""
Enter the physiological features below to predict the progression score of the disease. 
Values should be normalized (standardized) as per the dataset requirements.
""")

# Create two columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", value=0.05, format="%.4f")
    sex = st.number_input("Sex", value=0.05, format="%.4f")
    bmi = st.number_input("BMI", value=0.06, format="%.4f")
    bp = st.number_input("BP (Blood Pressure)", value=0.02, format="%.4f")
    s1 = st.number_input("S1 (Serum 1)", value=-0.04, format="%.4f")

with col2:
    s2 = st.number_input("S2 (Serum 2)", value=-0.04, format="%.4f")
    s3 = st.number_input("S3 (Serum 3)", value=-0.02, format="%.4f")
    s4 = st.number_input("S4 (Serum 4)", value=-0.01, format="%.4f")
    s5 = st.number_input("S5 (Serum 5)", value=0.01, format="%.4f")
    s6 = st.number_input("S6 (Serum 6)", value=0.02, format="%.4f")

# Prediction Button
if st.button("Predict Progression Score"):
    # 1. Prepare the payload matching your PatientData Pydantic model
    payload = {
        "age": age, "sex": sex, "bmi": bmi, "bp": bp,
        "s1": s1, "s2": s2, "s3": s3, "s4": s4,
        "s5": s5, "s6": s6
    }

    try:
        # 2. Send POST request to FastAPI backend
        # Ensure your FastAPI server is running on port 8000
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            score = result["predicted_progression_socre"]
            interpretation = result["interpretation"]

            # 3. Display Results
            st.success(f"### Predicted Score: {score}")
            st.info(f"**Interpretation:** {interpretation}")
        else:
            st.error(f"Error: Received status code {response.status_code} from server.")
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Is it running?")