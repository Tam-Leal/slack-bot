# Dockerfile

# Use a specific version of the Python image from Docker Hub
FROM python:3.11-slim

# Define the working directory inside the container
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the local code to the container
COPY . .

# Install dependencies from requirements file
RUN pip3 install -r requirements.txt
RUN pip3 install -U python-dotenv

# Expose the port Streamlit runs on
EXPOSE $PORT

# Health check command to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:$PORT/_stcore/health || exit 1

# Use a shell form of CMD to use variable substitution correctly
CMD streamlit run main.py --server.enableWebsocketCompression=false --server.enableCORS=true --server.enableXsrfProtection=true --server.port=${PORT:-8501} --server.address=0.0.0.0
