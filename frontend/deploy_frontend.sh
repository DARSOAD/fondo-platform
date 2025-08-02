#!/bin/bash
set -e

STACK_NAME=frontend-stack
REGION=us-east-1
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET_NAME="nextjs-frontend-${ACCOUNT_ID}"

echo " Ejecutando build del frontend..."
npm install
npm run build
npx next export

echo " Desplegando infraestructura CloudFormation..."
aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --template-file ../cloudformation/frontend-template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region $REGION

echo " Limpiando contenido antiguo en el bucket..."
aws s3 rm s3://$BUCKET_NAME --recursive

echo " Subiendo el frontend (carpeta out/) a S3..."
aws s3 cp out/ s3://$BUCKET_NAME --recursive

echo " Sitio desplegado correctamente. URLs:"
aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --region $REGION \
  --query "Stacks[0].Outputs[*].[OutputKey,OutputValue]" \
  --output table
