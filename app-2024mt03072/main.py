import os  # Importing os module to interact with the operating system
from fastapi import FastAPI  # Importing FastAPI to create the web application
from fastapi.responses import Response  # Importing Response to send custom HTTP responses
from contextlib import asynccontextmanager  # Importing asynccontextmanager to manage application lifespan
from pydantic_settings import BaseSettings  # Importing BaseSettings to manage application configuration
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST  # Importing Prometheus client for metrics

# Defining a Settings class to manage application settings using environment variables
class Settings(BaseSettings):
    APP_VERSION: str = "1.0"    # Setting the default application version
    APP_TITLE: str = "My FastAPI App"   # Setting the default application title

    # Config class to specify additional configuration options for the Settings class
    class Config:
        env_file = ".env"   # Specifying the environment file to load variables from while running locally

settings = Settings()   # Creating an instance of the Settings class to access configuration values

POD_NAME = os.getenv("POD_NAME", "unknown")  # Fetching the pod name from environment variables, defaulting to "unknown" if not set

# Defining Prometheus metric to count requests to the /get_info endpoint, labeled by pod
REQUEST_COUNT = Counter(
    'get_info_requests_total',    # Metric name
    'Total number of requests to /get_info endpoint',  # Metric description
    ['pod']   # Label to differentiate metrics by pod
)

# Lifespan context manager to manage application startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # Run the app

# Creating an instance of the FastAPI application with a custom lifespan
app = FastAPI(lifespan=lifespan)

# Defining a route to handle GET requests at the "/get_info" endpoint
@app.get("/get_info")
async def get_info():
    REQUEST_COUNT.labels(pod=POD_NAME).inc()  # Increment the request count metric for this pod
    # Returning a JSON response with application version, title, and pod name
    return {
        "APP_VERSION": settings.APP_VERSION,  # Fetching the application version from settings
        "APP_TITLE": settings.APP_TITLE,      # Fetching the application title from settings
        "POD_NAME": POD_NAME                  # Including the pod name in the response
    }
