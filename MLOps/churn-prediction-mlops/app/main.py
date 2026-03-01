import pandas as pd
from collections import Counter

import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.utils.logger import get_logger

logger = get_logger()

app = FastAPI(title="Churn Prediction API with Shadow Deployment")

# -----------------------------
# Global State
# -----------------------------
model = None
model_info = None

shadow_model = None
shadow_model_info = None

request_metrics = Counter()

client = MlflowClient()


# -----------------------------
# Startup: Load Models
# -----------------------------
@app.on_event("startup")
def load_models():
    global model, model_info
    global shadow_model, shadow_model_info

    try:
        # -----------------------------
        # Load Production Model (Alias)
        # -----------------------------
        model = mlflow.pyfunc.load_model(
            model_uri="models:/ChurnModel@production"
        )

        model_info = client.get_model_version_by_alias(
            name="ChurnModel",
            alias="production"
        )

        logger.info(
            f"Production model loaded. Version: {model_info.version}"
        )

        # -----------------------------
        # Load Latest Version as Shadow
        # -----------------------------
        all_versions = client.search_model_versions(
            "name='ChurnModel'"
        )

        latest_version = max(
            all_versions,
            key=lambda v: int(v.version)
        )

        if latest_version.version != model_info.version:
            shadow_model = mlflow.pyfunc.load_model(
                model_uri=f"models:/ChurnModel/{latest_version.version}"
            )
            shadow_model_info = latest_version

            logger.info(
                f"Shadow model loaded. Version: {shadow_model_info.version}"
            )
        else:
            logger.info("No shadow model available.")

    except Exception as e:
        logger.warning(f"Model loading failed: {str(e)}")


# -----------------------------
# Request Schema
# -----------------------------
class InputData(BaseModel):
    feature1: float
    feature2: float


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Churn Prediction API is live 🚀"}


# -----------------------------
# Prediction Endpoint
# -----------------------------
@app.post("/predict")
def predict(data: InputData):

    request_metrics["total_requests"] += 1

    if model is None:
        request_metrics["failed_requests"] += 1
        raise HTTPException(status_code=503, detail="Production model not loaded")

    try:
        # ✅ Use Pandas DataFrame (removes sklearn warning)
        input_df = pd.DataFrame(
            [[data.feature1, data.feature2]],
            columns=["feature1", "feature2"]
        )

        # -----------------------------
        # Production Prediction
        # -----------------------------
        prod_prediction = model.predict(input_df)[0]
        request_metrics["successful_predictions"] += 1

        logger.info(
            f"Prod v{model_info.version} prediction: {prod_prediction}"
        )

        # -----------------------------
        # Shadow Prediction
        # -----------------------------
        if shadow_model:
            shadow_prediction = shadow_model.predict(input_df)[0]

            logger.info(
                f"Shadow v{shadow_model_info.version} prediction: {shadow_prediction}"
            )

            request_metrics["shadow_requests"] += 1

            if shadow_prediction != prod_prediction:
                request_metrics["shadow_disagreements"] += 1
                logger.warning(
                    f"Disagreement detected | "
                    f"Prod: {prod_prediction} | Shadow: {shadow_prediction}"
                )

        return {"prediction": int(prod_prediction)}

    except Exception as e:
        request_metrics["failed_requests"] += 1
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")


# -----------------------------
# Metrics Endpoint
# -----------------------------
@app.get("/metrics")
def metrics():

    disagreement_rate = 0

    if request_metrics["shadow_requests"] > 0:
        disagreement_rate = (
            request_metrics["shadow_disagreements"]
            / request_metrics["shadow_requests"]
        )

    return {
        "total_requests": request_metrics["total_requests"],
        "successful_predictions": request_metrics["successful_predictions"],
        "failed_requests": request_metrics["failed_requests"],
        "current_production_version": model_info.version if model_info else None,
        "shadow_version": shadow_model_info.version if shadow_model_info else None,
        "shadow_requests": request_metrics["shadow_requests"],
        "shadow_disagreements": request_metrics["shadow_disagreements"],
        "shadow_disagreement_rate": disagreement_rate
    }