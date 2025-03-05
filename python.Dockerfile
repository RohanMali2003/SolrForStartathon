# Use an official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy your Python app
COPY python-app /app

# Install dependencies
RUN pip install -r requirements.txt

# Run your Python script
CMD ["python", "solr_connector.py"]
