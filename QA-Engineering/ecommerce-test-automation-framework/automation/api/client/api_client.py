import requests
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class APIClient:

    def __init__(self):
        self.base_url = Config.API_BASE_URL

    def get(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to {url}")
        response = requests.get(url)
        return response

    def post(self, endpoint: str, payload: dict):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to {url}")
        response = requests.post(url, json=payload)
        return response