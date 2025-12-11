Campaign Metrics API

The Campaign Metrics API is a lightweight Flask microservice that returns simulated marketing campaign metrics. It was built to demonstrate containerization, cloud deployment, and DevOps workflows using Docker, Azure Container Registry, Azure Container Apps, and GitHub version control. The service runs publicly in Azure and exposes simple REST endpoints that return randomized impressions, clicks, and conversions similar to analytics data used in reporting dashboards.

This project uses Python 3.11, Flask, Docker Buildx, Azure Container Registry, Azure Container Apps, and GitHub. The API includes the following endpoints:

GET /
Returns a message confirming that the API is running.

GET /health
Used by Azure for health and readiness checks.

GET /metrics
Returns simulated metrics such as impressions, clicks, conversions, and the container host name.

The Docker image is built and pushed using multi-architecture Docker Buildx. Example build command:

docker buildx build --platform linux/amd64 -t <registry>/campaign-metrics-api:<tag> --push .


The application is deployed to Azure Container Apps with external ingress on port 5050. The image is updated using:

az containerapp update --name campaign-api --resource-group devops-rg --image <registry>/campaign-metrics-api:<tag>


To restart the active revision:

REV=$(az containerapp show --name campaign-api --resource-group devops-rg --query "properties.latestRevisionName" -o tsv)
az containerapp revision restart --name campaign-api --resource-group devops-rg --revision $REV


To view logs:

az containerapp logs show --name campaign-api --resource-group devops-rg --revision $REV --follow


Project structure includes app.py, Dockerfile, requirements.txt, .gitignore, and README.md. For local development, install dependencies with pip install -r requirements.txt and run the app with python app.py at http://localhost:5050.

A CI/CD pipeline can be added using GitHub Actions to automatically build the Docker image and deploy the updated container to Azure Container Apps. The workflow file (.github/workflows/deploy.yml) builds and pushes the latest image and then triggers an Azure deployment using service principal credentials stored as GitHub secrets.

This project is licensed under the MIT License.
