# campaign-metrics-api
Campaign Metrics API
Overview

The Campaign Metrics API is a lightweight Flask-based microservice that returns simulated campaign analytics metrics. It is designed to demonstrate DevOps skills including containerization, multi-architecture Docker builds, Azure deployment, logging, and revision management.

This service exposes simple REST endpoints and returns randomized metrics that could represent advertising performance data used in dashboards or analytics pipelines.

Tech Stack

Python 3.11

Flask

Docker and Docker Buildx

Azure Container Registry (ACR)

Azure Container Apps

GitHub version control

API Endpoints
GET /

Returns a simple message indicating the service is running.

Example:

Campaign Metrics API is running

GET /health

Used by Azure Container Apps for health checks.

Example:

{
  "status": "ok"
}

GET /metrics

Returns simulated advertising metrics.

Example:

{
  "impressions": 3877,
  "clicks": 282,
  "conversions": 22,
  "host": "campaign-api--0000008-86cfb5647c-cwtbd"
}

Docker Usage
Build and push an amd64 Docker image
docker buildx build \
  --platform linux/amd64 \
  -t <registry>/campaign-metrics-api:<tag> \
  --push .


Example:

docker buildx build \
  --platform linux/amd64 \
  -t gloriaacr.azurecr.io/campaign-metrics-api:1.0.4 \
  --push .

Azure Deployment

This service is deployed using Azure Container Apps with:

ACR for container storage

Ingress on port 5050

Single active revision mode

Update the running container image
az containerapp update \
  --name campaign-api \
  --resource-group devops-rg \
  --image gloriaacr.azurecr.io/campaign-metrics-api:<tag>

Restart the active revision
REV=$(az containerapp show \
  --name campaign-api \
  --resource-group devops-rg \
  --query "properties.latestRevisionName" -o tsv)

az containerapp revision restart \
  --name campaign-api \
  --resource-group devops-rg \
  --revision $REV

View Logs
az containerapp logs show \
  --name campaign-api \
  --resource-group devops-rg \
  --revision $REV \
  --follow

Project Structure
campaign-metrics-api/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md

Local Development

Install dependencies:

pip install -r requirements.txt


Run locally:

python app.py


Default local URL:

http://localhost:5050

License

This project is released under the MIT License.

CI/CD Pipeline (GitHub Actions)

Create this file:

.github/workflows/deploy.yml

Paste the following:

name: Build and Deploy to Azure Container Apps

on:
  push:
    branches:
      - main

env:
  REGISTRY: gloriaacr.azurecr.io
  IMAGE_NAME: campaign-metrics-api
  RESOURCE_GROUP: devops-rg
  CONTAINER_APP: campaign-api

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Log in to Azure Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.ACR_USERNAME }}
        password: ${{ secrets.ACR_PASSWORD }}

    - name: Build and push image
      run: |
        docker buildx build \
          --platform linux/amd64 \
          -t $REGISTRY/$IMAGE_NAME:latest \
          --push .

    - name: Deploy to Azure Container Apps
      run: |
        az containerapp update \
          --name $CONTAINER_APP \
          --resource-group $RESOURCE_GROUP \
          --image $REGISTRY/$IMAGE_NAME:latest
