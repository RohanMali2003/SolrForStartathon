# Use an official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy Python app files
COPY python-app /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports (if any)
EXPOSE 5000  # Adjust based on your app's needs

# Run the Python script
CMD ["python3", "solr_connector.py"]
