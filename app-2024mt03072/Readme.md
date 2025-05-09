# FastAPI Application Deployment with Docker, Kubernetes, and Prometheus  
**Author:** 2024MT03072

---

## 1. Local Setup and FastAPI Development
```bash
# Create and navigate into project directory
mkdir app-2024mt03072
cd app-2024mt03072

# Set up Python virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies and run FastAPI app
pip install -r requirements.txt
uvicorn main:app --reload --port 8000


# Install Docker
sudo apt-get install -y docker.io
sudo systemctl enable --now docker

# Build Docker image for FastAPI app
docker build -t img-2024mt03072:dev .

# List available images
docker images


# Run Docker container with port forwarding
docker run -d --name cnr-2024mt03072 -p 8000:8000 img-2024mt03072:dev

# Check running containers and logs
docker ps
docker logs cnr-2024mt03072


# Download and install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikubelinux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start and check status
minikube start
minikube status

# Load image into Minikube’s Docker environment
minikube image load img-2024mt03072:dev

# Apply Kubernetes configuration
minikube kubectl -- apply -f fastapi-namespace-2024mt03072.yaml
minikube kubectl -- get namespaces

minikube kubectl -- apply -f fastapi-config-2024mt03072.yaml
minikube kubectl -- get configmaps -n ns-fastapi-2024mt03072

minikube kubectl -- apply -f fastapi-deployment-2024mt03072.yaml
minikube kubectl -- get deployments -n ns-fastapi-2024mt03072
minikube kubectl -- get pods -n ns-fastapi-2024mt03072


# Create and expose FastAPI service
minikube kubectl -- apply -f fastapi-service-2024mt03072.yaml
minikube kubectl -- get services -n ns-fastapi-2024mt03072
minikube service fastapi-service -n ns-fastapi-2024mt03072 --url

# Simulate traffic to test FastAPI response
for i in {1..2000}; do
  echo -n "Request #$i: "
  curl -s http://192.168.49.2:31048/get_info
  echo
  sleep 1
done


# Reinstall Python dependencies if required
pip install -r requirements.txt

# Deploy Prometheus configuration and services
minikube kubectl -- apply -f prometheus-config-2024mt03072.yaml
minikube kubectl -- get configmaps -n ns-fastapi-2024mt03072

minikube kubectl -- apply -f prometheus-deployment-2024mt03072.yaml
minikube kubectl -- get deployments -n ns-fastapi-2024mt03072
minikube kubectl -- get pods -n ns-fastapi-2024mt03072

minikube kubectl -- apply -f prometheus-service-2024mt03072.yaml
minikube kubectl -- get services -n ns-fastapi-2024mt03072
minikube service prometheus -n ns-fastapi-2024mt03072 --url


get_info_requests_total
container_cpu_usage_seconds_total{namespace="ns-fastapi-2024mt03072"}
container_memory_usage_bytes{namespace="ns-fastapi-2024mt03072"} / (1024 * 1024)
