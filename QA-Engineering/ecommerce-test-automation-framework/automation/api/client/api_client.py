import requests
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class APIClient:

    def __init__(self):
        self.base_url = Config.API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (QA-Automation-Framework)",
            "Accept": "application/json"
        })

    def get(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to {url}")
        response = self.session.get(url, timeout=10)
        return response

    def post(self, endpoint: str, payload: dict):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to {url}")
        response = self.session.post(url, json=payload, timeout=10)
        return response