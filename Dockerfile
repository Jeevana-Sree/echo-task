FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tzdata 

COPY backend/ /app
COPY frontend/ /app/../frontend

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
