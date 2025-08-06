#!/bin/sh
set -e

# Por defecto: entorno cloud
ENVIRONMENT=${ENVIRONMENT:-cloud}

if [ "$ENVIRONMENT" = "local" ]; then
  echo " Esperando a que DynamoDB Local esté disponible..."
  until curl -s http://dynamodb-local:8000; do
    >&2 echo " DynamoDB aún no responde - esperando..."
    sleep 2
  done

  echo " DynamoDB disponible. Ejecutando create_table.py..."
  python create_table.py
else
  echo " Entorno cloud detectado. No se usará DynamoDB Local."
fi

echo " Iniciando servidor FastAPI con Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
