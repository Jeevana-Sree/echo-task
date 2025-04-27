FROM python:3.9-slim

WORKDIR /app

# Install tzdata for timezone support only
RUN apt-get update && apt-get install -y \
    tzdata 

# Copy backend and frontend code
COPY backend/ /app
COPY frontend/ /app/../frontend

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "app.py"]
