# User clicks → FastAPI → Kinesis → Lambda → S3 (JSON files) (Bronze Layer)

# Add Trigger → Source: Kinesis

import json
import base64
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = "uber-data-lake-pooja"

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)

        file_name = f"bronze/streaming/{datetime.utcnow().isoformat()}_{uuid.uuid4()}.json"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(data)
        )

    return {
        'statusCode': 200,
        'body': 'Success'
    }

# Verify in S3 → bronze/streaming/