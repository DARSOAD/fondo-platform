import boto3
import os

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8001"),
    region_name=os.getenv("AWS_REGION", "us-west-2"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "fakeMyKeyId"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "fakeSecretKey")
)
