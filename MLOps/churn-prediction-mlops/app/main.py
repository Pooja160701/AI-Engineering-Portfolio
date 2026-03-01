from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from src.utils.logger import get_logger
from fastapi import HTTPException

logger = get_logger()

app = FastAPI(title="Churn Prediction API")

model = joblib.load("artifacts/model.pkl")

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
    try:
        logger.info("Prediction request received")

        input_array = np.array([[data.feature1, data.feature2]])
        prediction = model.predict(input_array)[0]

        return {"prediction": int(prediction)}

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")