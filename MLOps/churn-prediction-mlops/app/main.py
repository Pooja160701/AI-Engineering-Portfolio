from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi import HTTPException
from src.utils.logger import get_logger
import os
import mlflow.pyfunc
from mlflow.tracking import MlflowClient

logger = get_logger()
client = MlflowClient()

app = FastAPI(title="Churn Prediction API")

model = None  # global placeholder


@app.on_event("startup")
def load_model():
    global model

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

    mlflow.set_tracking_uri(f"sqlite:///{PROJECT_ROOT}/mlflow.db")

    try:
        model = mlflow.pyfunc.load_model(
            model_uri="models:/ChurnModel@production"
        )
        logger.info("Production model loaded from MLflow registry.")

        model_info = client.get_model_version_by_alias(
            name="ChurnModel",
            alias="production"
        )
        logger.info(f"Currently serving model version {model_info.version} with status: {model_info.status}")
        
    except Exception as e:
        logger.warning(f"Model load failed: {str(e)}")
        model = None


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