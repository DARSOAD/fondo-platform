import boto3
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8001"),
    region_name=os.getenv("AWS_REGION", "us-west-2"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "fakeMyKeyId"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "fakeSecretKey")
)

def create_table():
    try:
        table = dynamodb.create_table(
            TableName='transacciones',
            KeySchema=[
                {'AttributeName': 'usuario_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'usuario_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print("✅ Tabla 'transacciones' creada correctamente.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("ℹ️ La tabla 'transacciones' ya existe.")
        else:
            raise

if __name__ == "__main__":
    create_table()
