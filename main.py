import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

# Load trained pipeline
model = joblib.load("heart_disease_pipeline.joblib")

# Enums for categorical fields
class SexEnum(str, Enum):
    male = "Male"
    female = "Female"

class BinaryEnum(str, Enum):
    yes = "Yes"
    no = "No"

class RestECGEnum(str, Enum):
    normal = "Normal"
    stt_abnormality = "ST-T wave abnormality"
    lv_hypertrophy = "Left ventricular hypertrophy"

class SlopeEnum(str, Enum):
    upsloping = "Upsloping"
    flat = "Flat"
    downsloping = "Downsloping"

class ThalEnum(str, Enum):
    normal = "Normal"
    fixed_defect = "Fixed defect"
    reversible_defect = "Reversible defect"

class ChestPainEnum(str, Enum):
    typical_angina = "Typical angina"
    atypical_angina = "Atypical angina"
    non_anginal_pain = "Non-anginal pain"
    asymptomatic = "Asymptomatic"

# Request model
class PatientData(BaseModel):
    age: int
    sex: SexEnum
    cp: ChestPainEnum
    trestbps: float
    chol: float
    fbs: BinaryEnum
    restecg: RestECGEnum
    thalch: float
    exang: BinaryEnum
    oldpeak: float
    slope: SlopeEnum
    ca: float
    thal: ThalEnum

# Root/Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Prediction endpoint
@app.post("/predict")
def predict_heart_disease(data: PatientData):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = model.predict(df)[0]
        risk = "High" if prediction == 1 else "Low"
        return {
            "prediction": int(prediction),
            "risk": risk
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
