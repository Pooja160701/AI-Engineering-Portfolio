import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "uber-stream")

kinesis_client = boto3.client(
    "kinesis",
    region_name="us-east-1",
)


def send_to_kinesis(ride_data=None):
    try:
        response = kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(ride_data),
            PartitionKey=ride_data["ride_id"]
        )

        print("Sent to Kinesis:", response["SequenceNumber"])
        return "Sent to Kinesis"

    except Exception as e:
        print("Error:", str(e))
        return False