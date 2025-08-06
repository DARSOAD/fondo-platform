
# Plataforma Técnica de Fondos de Inversión – Prueba Amaris

Este proyecto implementa una solución completa para la gestión de suscripciones a fondos de inversión, incluyendo backend (FastAPI + DynamoDB) y frontend (Next.js + Tailwind CSS), con despliegue automatizado vía Docker y AWS CloudFormation.

## Tecnologías utilizadas

- Backend: FastAPI, DynamoDB, Pydantic, Pytest
- Frontend: Next.js, Tailwind CSS, React Hook Form, Zod, Axios, Context API
- Infraestructura: Docker, CloudFormation

## Funcionalidades clave

- Suscripción a fondos
- Cancelación de suscripción
- Consulta de historial de transacciones
- Cálculo de saldo actual
- Validación y pruebas automatizadas
- Despliegue local y en la nube

## Ejecución local

```bash
# Levantar backend y base de datos local
docker-compose up --build

# Build del frontend y prueba local
cd frontend
npm install
npm run build
npx serve out
```

## Despliegue en AWS (CloudFormation)

```bash
# Desplegar infraestructura frontend y subir archivos
cd frontend
bash deploy_frontend.sh
```

Las URLs de acceso serán impresas automáticamente al finalizar.

## Documentación técnica

La documentación completa del modelo de datos, decisiones de arquitectura, justificación de tecnologías, estructura del proyecto y declaración de uso de IA se encuentra disponible en:

[manual_tecnico_fondos_amaris.pdf]

##### CloudFormation ######

### BackEnd

## ✅ Requisitos previos

Antes de desplegar, asegúrate de tener:

- AWS CLI configurado (`aws configure`)
- Una imagen Docker funcional (`fondos-backend`)
- Un repositorio en Amazon ECR privado
- Permisos para crear roles, tablas y servicios (`CAPABILITY_NAMED_IAM`)
- El archivo `backend-template.yaml` dentro de la carpeta `cloudformation/`

---

## 🐳 1. Construir y subir la imagen Docker a Amazon ECR

Desde la carpeta raíz del proyecto (donde está el `Dockerfile`):

```bash
# Construir la imagen
docker build -t fondos-backend .

# Etiquetar la imagen con tu repositorio ECR (reemplaza por tu ID)
docker tag fondos-backend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/fondos-backend:latest

# Autenticarse con ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Subir la imagen
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/fondos-backend:latest
```

---

## 🚀 2. Despliegue del backend con CloudFormation

Desde la carpeta del proyecto:

```bash
cd cloudformation
```

Luego ejecuta:

```powershell
aws cloudformation deploy `
  --template-file backend-template.yaml `
  --stack-name fondos-backend-stack `
  --capabilities CAPABILITY_NAMED_IAM
```

> 💡 Si estás en Linux o macOS, reemplaza los backticks `\`` por barra invertida `\`.

---

#### FrontEnd

## 🌐 Variables de entorno

Asegúrate de crear un archivo `.env.production` en la carpeta `frontend/` con el siguiente contenido:

```env
NEXT_PUBLIC_API_URL=https://bzmy2vsin3.us-east-1.awsapprunner.com
```

Esto permite que el frontend conozca la URL del backend desplegado en App Runner.

---

## 🚀 Despliegue del frontend

Desde la carpeta `/frontend`, ejecuta el siguiente script para compilar y desplegar automáticamente todo:

```bash
./deploy_frontend.sh
```

El script realiza las siguientes acciones:

1. Compila el proyecto (`npm run build`) con variables de entorno de producción
2. Despliega la infraestructura en AWS con CloudFormation
3. Sube el contenido generado a S3
4. Invalida la caché de CloudFront para reflejar los últimos cambios

---

## 🔗 Acceso al sitio

Una vez finalizado el despliegue, puedes encontrar la URL pública del frontend en la consola de AWS:

1. Ve al servicio **CloudFormation**
2. Selecciona el stack `frontend-stack`
3. Abre la pestaña `Outputs`
4. Copia el valor de `CloudFrontURL`

---

## 📂 Comando alternativo para subir archivos manualmente (opcional)

Si necesitas sincronizar manualmente la carpeta generada con S3:

```bash
aws s3 sync out/ s3://nextjs-frontend-<tu-account-id> --delete
```

---
