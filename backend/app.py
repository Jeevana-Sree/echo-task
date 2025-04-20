from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import spacy
import psycopg2
from dateutil import parser
from flask_cors import CORS
from zoneinfo import ZoneInfo 

# Correct app setup
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
scheduler = BackgroundScheduler()
scheduler.start()

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="echodb",
    user="postgres",
    password="Pandu@2k3",
    host="db",
    port="5432"
)
cur = conn.cursor()

# Create tasks table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        task TEXT,
        time TIMESTAMP
    )
""")
conn.commit()

# Function to schedule voice reminder
def schedule_reminder(task, time):
    def speak():
        tts = gTTS(f"Reminder: {task}")
        tts.save("reminder.mp3")
        os.system("start reminder.mp3" if os.name == "nt" else "mpg123 reminder.mp3")
    scheduler.add_job(speak, trigger='date', run_date=time)

# Serve index.html from frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Endpoint to return saved tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cur.execute("SELECT task, time FROM tasks ORDER BY time ASC")
    tasks = cur.fetchall()
    return jsonify(tasks)


@app.route('/submit-task', methods=['POST'])
def submit_task():
    data = request.get_json()
    text = data.get("text", "").strip()

    # Make it case-insensitive
    if " at " not in text.lower() or "remind me to" not in text.lower():
        return jsonify({"error": "Invalid format. Say: 'Remind me to [task] at [time]'"}), 400

    try:
        # Normalize text to lowercase for parsing but preserve original casing for task
        lower_text = text.lower()
        split_index = lower_text.index(" at ")
        task = text[len("Remind me to "):split_index].strip()
        time_str = text[split_index + 4:].strip()
        
        # Parse and localize to IST
        time = parser.parse(time_str)
        time = time.replace(tzinfo=ZoneInfo("Asia/Kolkata"))

    except Exception as e:
        return jsonify({"error": "Could not parse task or time"}), 400

    # Save to DB
    cur.execute("INSERT INTO tasks (task, time) VALUES (%s, %s)", (task, time))
    conn.commit()

    schedule_reminder(task, time)
    return jsonify({"message": "Task saved and reminder set"}), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
