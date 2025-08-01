# backend/db/dynamodb.py
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://localhost:9000",  
    region_name="us-west-2",
    aws_access_key_id="fakeMyKeyId",       
    aws_secret_access_key="fakeSecretKey"  
)


