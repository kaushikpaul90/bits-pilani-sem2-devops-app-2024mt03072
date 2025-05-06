import os  # Importing os module to interact with the operating system
import time  # Importing time module for time-related operations
import psutil  # Importing psutil to collect system metrics like CPU and memory usage
import threading  # Importing threading to run background tasks
from fastapi import FastAPI  # Importing FastAPI to create the web application
from fastapi.responses import Response  # Importing Response to send custom HTTP responses
from contextlib import asynccontextmanager  # Importing asynccontextmanager to manage application lifespan
from pydantic_settings import BaseSettings  # Importing BaseSettings to manage application configuration
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST  # Importing Prometheus client for metrics

# Defining a Settings class to manage application settings using environment variables
class Settings(BaseSettings):
    APP_VERSION: str = "1.0"    # Setting the default application version
    APP_TITLE: str = "My FastAPI App"   # Setting the default application title

    # Config class to specify additional configuration options for the Settings class
    class Config:
        env_file = ".env"   # Specifying the environment file to load variables from while running locally

settings = Settings()   # Creating an instance of the Settings class to access configuration values

# Defining Prometheus metrics
REQUEST_COUNT = Counter('get_info_requests_total', 'Total number of /get_info requests')  # Metric: Counts the total number of requests to the /get_info endpoint
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage', ['pod'])  # Metric: Tracks CPU usage percentage, labeled by pod
MEMORY_USAGE = Gauge('memory_usage_mb', 'Memory usage in MB', ['pod'])  # Metric: Tracks memory usage in MB, labeled by pod

POD_NAME = os.getenv("POD_NAME", "unknown")  # Fetching the pod name from environment variables, defaulting to "unknown" if not set

# Function to collect system metrics (CPU and memory usage) periodically
def collect_system_metrics():
    while True:
        # Updating CPU usage metric
        CPU_USAGE.labels(pod=POD_NAME).set(psutil.cpu_percent(interval=1))
        # Updating memory usage metric
        MEMORY_USAGE.labels(pod=POD_NAME).set(psutil.virtual_memory().used / (1024 * 1024))
        time.sleep(5)  # Sleep for 5 seconds before collecting metrics again

# Lifespan context manager to manage application startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start system metrics collection in a separate thread
    thread = threading.Thread(target=collect_system_metrics, daemon=True)
    thread.start()
    yield  # Run the app

# Creating an instance of the FastAPI application with a custom lifespan
app = FastAPI(lifespan=lifespan)

# Defining a route to handle GET requests at the "/get_info" endpoint
@app.get("/get_info")
async def get_info():
    REQUEST_COUNT.inc()  # Increment the request count metric
    pod_name = POD_NAME  # Fetching the pod name from the environment variable
    # Returning a JSON response with application version, title, and pod name
    return {
        "APP_VERSION": settings.APP_VERSION,  # Fetching the application version from settings
        "APP_TITLE": settings.APP_TITLE,      # Fetching the application title from settings
        "POD_NAME": pod_name                  # Including the pod name in the response
    }
