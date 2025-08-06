#!/bin/bash

set -e

# Compilar y exportar el frontend
export NEXT_PUBLIC_API_URL=https://bzmy2vsin3.us-east-1.awsapprunner.com
NODE_ENV=production npm run build

# Crear el stack (bucket + CDN)
aws cloudformation deploy \
  --template-file ../cloudformation/frontend-template.yaml \
  --stack-name frontend-stack \
  --capabilities CAPABILITY_NAMED_IAM

# Subir los archivos generados a S3
aws s3 sync out/ s3://nextjs-frontend-985898635541 --delete # Cambia el nombre del bucket según tu configuración

# Paso 4: (opcional) Invalidate CloudFront cache
DIST_ID=$(aws cloudformation describe-stacks \
  --stack-name frontend-stack \
  --query "Stacks[0].Outputs[?OutputKey=='CloudFrontURL'].OutputValue" \
  --output text | awk -F/ '{print $3}')

aws cloudfront create-invalidation \
  --distribution-id $DIST_ID \
  --paths "/*"
