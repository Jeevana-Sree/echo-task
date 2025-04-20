FROM python:3.9-slim

WORKDIR /app

# Install build tools and tzdata for timezone support
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy backend and frontend code
COPY backend/ /app
COPY frontend/ /app/../frontend

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Run the app
CMD ["python", "app.py"]
