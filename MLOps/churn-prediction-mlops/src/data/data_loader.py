import pandas as pd
from src.utils.logger import get_logger

logger = get_logger()

def load_data(path: str) -> pd.DataFrame:
    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path)
    logger.info(f"Data shape: {df.shape}")
    return df