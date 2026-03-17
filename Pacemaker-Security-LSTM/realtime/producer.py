import json
import random
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:

    patient_data = {
        "BMI": random.uniform(18,40),
        "Smoking": random.randint(0,1),
        "Alcohol": random.randint(0,1),
        "Stroke": random.randint(0,1),
        "Sex": random.randint(0,1),
        "Age_Category": random.randint(0,10),
        "Diabetic": random.randint(0,1),
        "PhysicalActivity": random.randint(0,1),
        "HeartRate": random.randint(60,110)
    }

    producer.send("pacemaker_signals", patient_data)

    print("Sent:", patient_data)

    time.sleep(2)