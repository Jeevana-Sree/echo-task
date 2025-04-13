# Use a slim Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy dependency file first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY ./app ./app
COPY ./tests ./tests
COPY .env .

# Set the Python path so tests can import app modules
ENV PYTHONPATH=/app

# Expose the Flask port
EXPOSE 5050

# Set the entry point
CMD ["python", "app/main.py"]
