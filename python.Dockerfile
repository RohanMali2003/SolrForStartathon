# Use an official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python app
COPY python-app /app

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Run the Python script with the correct input file
CMD ["python3", "/app/solr_connector.py", "/app/inputs.txt"]
