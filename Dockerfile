# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and folders explicitly
COPY app/ app/
COPY templates/ templates/
COPY static/ static/

# Expose port
EXPOSE 5050

# Run the Flask app
CMD ["python", "app/main.py"]
