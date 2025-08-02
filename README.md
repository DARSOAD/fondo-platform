
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
