from kafka import KafkaConsumer
import json
from inference import predict

consumer = KafkaConsumer(
    "pacemaker_signals",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

for message in consumer:

    patient = message.value

    result = predict(list(patient.values()))

    if result != 0:
        print("ALERT: Pacemaker anomaly detected")

    else:
        print("Normal heartbeat")