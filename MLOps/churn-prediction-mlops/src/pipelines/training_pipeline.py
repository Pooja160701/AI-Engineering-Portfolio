import yaml
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn

from src.data.data_loader import load_data
from src.utils.logger import get_logger

logger = get_logger()

def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)

def run_training():
    config = load_config()

    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    with mlflow.start_run():

        df = load_data(config["data"]["raw_data_path"])

        X = df.drop("target", axis=1)
        y = df["target"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=config["model"]["test_size"],
            random_state=config["model"]["random_state"]
        )

        model = RandomForestClassifier(
            random_state=config["model"]["random_state"]
        )

        model.fit(X_train, y_train)

        accuracy = model.score(X_test, y_test)

        logger.info(f"Model Accuracy: {accuracy}")

        mlflow.log_metric("accuracy", accuracy)

        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="ChurnModel"
        )

        os.makedirs("artifacts", exist_ok=True)
        joblib.dump(model, "artifacts/model.pkl")

        logger.info("Training completed successfully.")