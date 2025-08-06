# backend/services/notificacion_service.py

import boto3
import os

ses_client = boto3.client("ses", region_name=os.getenv("AWS_REGION", "us-east-1"))
sns_client = boto3.client("sns", region_name=os.getenv("AWS_REGION", "us-east-1"))

def enviar_notificacion( medio: str, mensaje: str, usuario_contacto: str):
    if medio == "email":
        response = ses_client.send_email(
            Source=os.getenv("SES_SOURCE_EMAIL"),  
            Destination={"ToAddresses": [usuario_contacto]},
            Message={
                "Subject": {"Data": "Confirmación de suscripción"},
                "Body": {"Text": {"Data": mensaje}},
            },
        )
        print(f"[SES] Email enviado a: {response['MessageId']}")

    elif medio == "sms":
        response = sns_client.publish(
            PhoneNumber=usuario_contacto,  
            Message=mensaje,
        )
        print(f"[SNS] SMS enviado a: {response['MessageId']}")

    else:
        raise ValueError("Medio de notificación no válido")
