# Importing FastAPI framework to create a web application
import os
from fastapi import FastAPI

# Importing BaseSettings from pydantic_settings to manage application configuration
from pydantic_settings import BaseSettings

# Defining a Settings class to manage application settings using environment variables
class Settings(BaseSettings):
    APP_VERSION: str = "1.0"    # Setting the default application version
    APP_TITLE: str = "My FastAPI App"   # Setting the default application title

    # Config class to specify additional configuration options for the Settings class
    class Config:
        env_file = ".env"   # Specifying the environment file to load variables from

settings = Settings()   # Creating an instance of the Settings class to access configuration values

app = FastAPI() # Creating an instance of the FastAPI application

# Defining a route to handle GET requests at the "/get_info" endpoint
@app.get("/get_info")
async def get_info():
    pod_name = os.environ.get("HOSTNAME", "unknown")    # Fetching the pod name from environment variables, defaulting to "unknown" if not set
    pod_ip = os.environ.get("POD_IP", "unknown")        # Fetching the pod IP from environment variables, defaulting to "unknown" if not set
    # Returning a JSON response with application version and title
    return {
        "APP_VERSION": settings.APP_VERSION,  # Fetching the application version from settings
        "APP_TITLE": settings.APP_TITLE,      # Fetching the application title from settings
        "POD_NAME": pod_name,    # Including the pod name in the response
        "POD_IP": pod_ip         # Including the pod IP in the response
    }
