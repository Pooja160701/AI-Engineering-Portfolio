import os
import yaml
import joblib
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from src.data.data_loader import load_data
from src.utils.logger import get_logger

logger = get_logger()


def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)
    

def run_training():
    config = load_config()

    # Set MLflow experiment
    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    client = MlflowClient()

    with mlflow.start_run() as run:

        # -----------------------------
        # Load & Prepare Data
        # -----------------------------
        df = load_data(config["data"]["raw_data_path"])

        X = df.drop("target", axis=1)
        y = df["target"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=config["model"]["test_size"],
            random_state=config["model"]["random_state"]
        )

        # -----------------------------
        # Train Model
        # -----------------------------
        model = RandomForestClassifier(
            random_state=config["model"]["random_state"]
        )

        model.fit(X_train, y_train)

        accuracy = model.score(X_test, y_test)

        logger.info(f"New Model Accuracy: {accuracy}")

        # Log metric
        mlflow.log_metric("accuracy", accuracy)

        # -----------------------------
        # Register Model
        # -----------------------------
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="ChurnModel"
        )

        # -----------------------------
        # Get Latest Registered Version
        # -----------------------------
        latest_versions = client.search_model_versions(
            "name='ChurnModel'"
        )

        latest_version = max(
            latest_versions,
            key=lambda v: int(v.version)
        )

        new_version = latest_version.version
        logger.info(f"New registered model version: {new_version}")

        # --------------------------------------------
        # 🚀 PRODUCTION COMPARISON LOGIC
        # --------------------------------------------

        try:
            production_version = client.get_model_version_by_alias(
                name="ChurnModel",
                alias="production"
            )

            prod_run = client.get_run(production_version.run_id)
            prod_accuracy = prod_run.data.metrics.get("accuracy", 0)

            logger.info(f"Production Model Accuracy: {prod_accuracy}")

            if accuracy > prod_accuracy:
                logger.info("New model is better. Promoting to Production.")

                client.set_registered_model_alias(
                    name="ChurnModel",
                    alias="production",
                    version=new_version
                )

            else:
                logger.info("New model is NOT better. Keeping existing production.")

        except Exception:
            logger.info("No production model found. Setting this as Production.")

            client.set_registered_model_alias(
                name="ChurnModel",
                alias="production",
                version=new_version
            )

        # -----------------------------
        # Save Local Artifact (Optional)
        # -----------------------------
        os.makedirs("artifacts", exist_ok=True)
        joblib.dump(model, "artifacts/model.pkl")

        logger.info("Training completed successfully.")