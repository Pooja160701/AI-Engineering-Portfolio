import random
import uuid
import json
from datetime import datetime, timedelta
from faker import Faker
import logging
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os

# Pulling Data Generator Function
from app.data import generate_uber_ride_confirmation

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
EVENT_HUBNAME = os.getenv("EVENT_HUBNAME")

def send_to_event_hub(ride_data=None):
    print("Mock send:", ride_data)
    return "Mock success"

if __name__ == "__main__":
    
    print("=" * 80)
    print("SINGLE RIDE CONFIRMATION")
    print("=" * 80)
    ride = generate_uber_ride_confirmation()
    print(json.dumps(ride, indent=2))

    print("\n" + "=" * 80)
    print("SENDING SINGLE RIDE TO EVENT HUB")
    result = send_to_event_hub(ride)
    print(f"Single ride sent to Event Hub: {result}")