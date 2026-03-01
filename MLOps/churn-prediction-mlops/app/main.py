from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi import HTTPException
from src.utils.logger import get_logger
import os
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
from collections import Counter

logger = get_logger()
client = MlflowClient()
request_metrics = Counter()

app = FastAPI(title="Churn Prediction API")

model = None
model_info = None

@app.on_event("startup")
def load_model():
    global model
    global model_info

    try:
        model_uri = "models:/ChurnModel@production"
        model = mlflow.pyfunc.load_model(model_uri)

        client = mlflow.tracking.MlflowClient()
        model_info = client.get_model_version_by_alias("ChurnModel", "production")

        logger.info("Production model loaded from MLflow registry.")
        logger.info(f"Currently serving model version {model_info.version} with status: {model_info.status}")

    except Exception as e:
        logger.warning(f"Model load failed: {str(e)}")


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

    request_metrics["total_requests"] += 1
    request_metrics["model_version"] = model_info.version

    if model is None:
        request_metrics["failed_requests"] += 1
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        input_array = np.array([[data.feature1, data.feature2]])
        prediction = model.predict(input_array)[0]

        request_metrics["successful_predictions"] += 1

        logger.info(f"Prediction made using model version {model_info.version}")

        return {"prediction": int(prediction)}

    except Exception as e:
        request_metrics["failed_requests"] += 1
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")
    

@app.get("/metrics")
def metrics():
    return {
        "total_requests": request_metrics["total_requests"],
        "successful_predictions": request_metrics["successful_predictions"],
        "failed_requests": request_metrics["failed_requests"],
        "current_model_version": model_info.version if model_info else None
    }