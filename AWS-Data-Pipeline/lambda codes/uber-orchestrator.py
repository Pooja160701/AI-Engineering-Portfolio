import boto3

athena = boto3.client('athena')

DATABASE = "uber"
OUTPUT = "s3://uber-data-lake-pooja/athena-results/"

def run_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            "Database": DATABASE
        },
        ResultConfiguration={
            "OutputLocation": OUTPUT
        },
        WorkGroup="primary"  
    )
    return response["QueryExecutionId"]


def lambda_handler(event, context):

    silver_query = "SELECT 1"
    gold_query = "SELECT 1"

    run_query(silver_query)
    run_query(gold_query)

    return {
        "statusCode": 200,
        "body": "Pipeline triggered"
    }

# Test Lambda
# Schedule with EventBridge [EventBridge → Rules → Create Rule]