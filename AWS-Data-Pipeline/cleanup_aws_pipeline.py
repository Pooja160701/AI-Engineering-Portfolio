import boto3
import time

REGION = "us-east-1"

lambda_client = boto3.client("lambda", region_name=REGION)
kinesis_client = boto3.client("kinesis", region_name=REGION)
s3 = boto3.resource("s3", region_name=REGION)
logs_client = boto3.client("logs", region_name=REGION)
scheduler = boto3.client("scheduler", region_name=REGION)

# -------- CONFIG --------
LAMBDA_NAME = "uber-orchestrator"
BUCKET_NAME = "uber-data-lake-pooja"
KINESIS_STREAM = "uber-stream"  # change if needed
SCHEDULE_NAME = "uber-pipeline-schedule"


# -------- DELETE SCHEDULER --------
def delete_scheduler():
    try:
        scheduler.delete_schedule(Name=SCHEDULE_NAME)
        print("✅ Scheduler deleted")
    except Exception as e:
        print("⚠️ Scheduler:", e)


# -------- DELETE LAMBDA --------
def delete_lambda():
    try:
        lambda_client.delete_function(FunctionName=LAMBDA_NAME)
        print("✅ Lambda deleted")
    except Exception as e:
        print("⚠️ Lambda:", e)


# -------- DELETE KINESIS --------
def delete_kinesis():
    try:
        kinesis_client.delete_stream(StreamName=KINESIS_STREAM, EnforceConsumerDeletion=True)
        print("✅ Kinesis deleted")
    except Exception as e:
        print("⚠️ Kinesis:", e)


# -------- DELETE S3 BUCKET --------
def delete_s3():
    try:
        bucket = s3.Bucket(BUCKET_NAME)
        bucket.objects.all().delete()
        bucket.delete()
        print("✅ S3 bucket deleted")
    except Exception as e:
        print("⚠️ S3:", e)


# -------- DELETE CLOUDWATCH LOGS --------
def delete_logs():
    try:
        log_group = f"/aws/lambda/{LAMBDA_NAME}"
        logs_client.delete_log_group(logGroupName=log_group)
        print("✅ CloudWatch logs deleted")
    except Exception as e:
        print("⚠️ Logs:", e)


# -------- MAIN --------
if __name__ == "__main__":
    print("🚀 Starting cleanup...\n")

    delete_scheduler()
    time.sleep(2)

    delete_lambda()
    time.sleep(2)

    delete_kinesis()
    time.sleep(5)

    delete_s3()
    time.sleep(2)

    delete_logs()

    print("\n🎉 Cleanup complete!")