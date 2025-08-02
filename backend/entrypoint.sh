#!/bin/bash
set -e

echo " Esperando a que DynamoDB Local esté disponible..."

# Espera hasta que DynamoDB responda en el puerto 8000
until curl -s http://dynamodb-local:8000; do
  >&2 echo " DynamoDB aún no responde - esperando..."
  sleep 2
done

echo " DynamoDB disponible. Ejecutando create_table.py..."
python create_table.py

echo " Iniciando servidor FastAPI con Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
