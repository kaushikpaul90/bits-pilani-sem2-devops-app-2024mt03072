# FastAPI Application Deployment with Docker, Kubernetes, and Prometheus  
**Author:** 2024MT03072

---

## **1. Local Setup and FastAPI Development**

```bash
# Create a new directory for the project
mkdir app-2024mt03072

# Navigate into the project directory
cd app-2024mt03072

# Create a Python virtual environment in the project
python -m venv .venv

# Activate the virtual environment (Linux/macOS)
source .venv/bin/activate

# Install all required Python packages from requirements.txt
pip install -r requirements.txt

# Start the FastAPI development server on port 8000
uvicorn main:app --reload --port 8000


## **2. Docker Image Creation**

```bash
# Install Docker using apt-get (Ubuntu/Debian systems)
sudo apt-get install -y docker.io

# Enable and start the Docker service immediately
sudo systemctl enable --now docker

# Build a Docker image with the tag 'img-2024mt03072:dev' from current directory
docker build -t img-2024mt03072:dev .

# List all Docker images on the system
docker images


## **3. Run and Monitor Docker Container**

```bash
# Run the Docker container in detached mode and map port 8000 of host to container
docker run -d --name cnr-2024mt03072 -p 8000:8000 img-2024mt03072:dev

# Show all currently running Docker containers
docker ps

# View logs from the running container named 'cnr-2024mt03072'
docker logs cnr-2024mt03072


## **4. Kubernetes Deployment with Minikube**

```bash
# Download latest Minikube binary for Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikubelinux-amd64

# Install the Minikube binary to /usr/local/bin
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube cluster
minikube start

# Check the status of Minikube cluster
minikube status

# Load the custom Docker image into Minikube’s local image registry
minikube image load img-2024mt03072:dev

# Apply a namespace configuration YAML file
minikube kubectl -- apply -f fastapi-namespace-2024mt03072.yaml

# List all namespaces to confirm creation
minikube kubectl -- get namespaces

# Apply FastAPI configmap YAML file
minikube kubectl -- apply -f fastapi-config-2024mt03072.yaml

# List configmaps in the custom namespace
minikube kubectl -- get configmaps -n ns-fastapi-2024mt03072

# Apply FastAPI deployment YAML file
minikube kubectl -- apply -f fastapi-deployment-2024mt03072.yaml

# List all deployments in the namespace
minikube kubectl -- get deployments -n ns-fastapi-2024mt03072

# List all pods in the namespace
minikube kubectl -- get pods -n ns-fastapi-2024mt03072


## **5. Expose FastAPI Service and Generate Load**

```bash
# Apply the FastAPI service YAML to expose the app
minikube kubectl -- apply -f fastapi-service-2024mt03072.yaml

# List all services in the namespace
minikube kubectl -- get services -n ns-fastapi-2024mt03072

# Get the external URL to access the service
minikube service fastapi-service -n ns-fastapi-2024mt03072 --url

# Simulate load on the FastAPI app by sending 2000 HTTP GET requests
for i in {1..2000}; do
  echo -n "Request #$i: "
  curl -s http://192.168.49.2:31048/get_info
  echo
  sleep 1
done


## **6. Monitoring with Prometheus**

```bash
# Reinstall Python dependencies if needed
pip install -r requirements.txt

# Apply Prometheus configmap YAML
minikube kubectl -- apply -f prometheus-config-2024mt03072.yaml

# List Prometheus configmaps in the namespace
minikube kubectl -- get configmaps -n ns-fastapi-2024mt03072

# Apply Prometheus deployment YAML
minikube kubectl -- apply -f prometheus-deployment-2024mt03072.yaml

# List deployments to confirm Prometheus is running
minikube kubectl -- get deployments -n ns-fastapi-2024mt03072

# List Prometheus pods
minikube kubectl -- get pods -n ns-fastapi-2024mt03072

# Apply Prometheus service YAML
minikube kubectl -- apply -f prometheus-service-2024mt03072.yaml

# List Prometheus services
minikube kubectl -- get services -n ns-fastapi-2024mt03072

# Get the URL for Prometheus UI
minikube service prometheus -n ns-fastapi-2024mt03072 --url

#### **Example Prometheus Queries**

# Total number of FastAPI /get_info requests
get_info_requests_total

# CPU usage for containers in the namespace
container_cpu_usage_seconds_total{namespace="ns-fastapi-2024mt03072"}

# Memory usage for containers in MB
container_memory_usage_bytes{namespace="ns-fastapi-2024mt03072"} / (1024 * 1024)
