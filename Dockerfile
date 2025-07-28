# Base image (lightweight & AMD64 compatible)
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app/ /app/

# Create input and output directories (for mounting)
RUN mkdir -p /app/input /app/output

# Command to run the script automatically when the container starts
CMD ["python", "main.py"]
