# Use the official Python 3.9 slim image as the base image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the main application file into the container
COPY main.py .

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for the application version and title
ENV APP_VERSION=1.0
ENV APP_TITLE="My Dockerized App"

# Expose port 8000 to allow external access to the application
EXPOSE 8000

# Define the command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]