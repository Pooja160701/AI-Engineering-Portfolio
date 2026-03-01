from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi import HTTPException
from src.utils.logger import get_logger
import os

logger = get_logger()

app = FastAPI(title="Churn Prediction API")

model = None  # global placeholder


@app.on_event("startup")
def load_model():
    global model
    model_path = "artifacts/model.pkl"

    if os.path.exists(model_path):
        model = joblib.load(model_path)
        logger.info("Model loaded successfully.")
    else:
        logger.warning("Model file not found. Running without loaded model.")


class InputData(BaseModel):
    feature1: float
    feature2: float


@app.get("/")
def root():
    return {"message": "Churn Prediction API is live"}


@app.get("/health")
def health():
    return {"status": "API is running"}


@app.post("/predict")
def predict(data: InputData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        input_array = np.array([[data.feature1, data.feature2]])
        prediction = model.predict(input_array)[0]
        return {"prediction": int(prediction)}

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")