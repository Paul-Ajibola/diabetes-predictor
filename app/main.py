
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.schema import PatientData
import pickle
import numpy as np
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="Diabetes Progression Predictor",
    description="Predicts Diabetes Progression Score from Physiological Features",
    version="1.0.0"
)

# Allow requests from the HTML frontend served on any localhost port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
model_path = os.path.join("models", "diabetes_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)



@app.get("/")
def homepage():
    index_path = os.path.join("app", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"Welcome to the Homepage!"}

# Mount static assets (style.css, script.js)
if os.path.exists("app"):
    app.mount("/static", StaticFiles(directory="app"), name="static")


@app.post("/predict")
def predict_progression(patient: PatientData):
    """
    Predict diabetes preogression score
    """
    # Convert input to numpy array
    features = np.array([[
        patient.age, patient.sex, patient.bmi, patient.bp,
        patient.s1, patient.s2, patient.s3, patient.s4,
        patient.s5, patient.s6
    ]])

    # Make Prediction
    prediction = model.predict(features)[0]

    # Return result with additional context
    return {
        "predicted_progression_socre": round(prediction, 2),
        "interpretation": get_interpretation(prediction)
    }

def get_interpretation(score):
    """
    provide human-readable interpretation of the score
    """
    if score < 100:
        return "Below average preogression"
    elif score < 150:
        return "Average progression"
    else:
        return "Above average progression"
    
@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "diabetes_progression_v1"}
