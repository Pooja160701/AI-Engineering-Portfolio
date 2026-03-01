import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://fakestoreapi.com")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", 5000))