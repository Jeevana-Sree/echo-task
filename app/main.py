from flask import Flask, request, jsonify
import psycopg2
import pyttsx3
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from threading import Lock
import os
import logging
from nlp import extract_task_and_time

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Flag to use TTS or not
USE_TTS = os.getenv("USE_TTS", "false").lower() == "true"
engine = pyttsx3.init() if USE_TTS else None

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.start()
scheduler_lock = Lock()

# Initialize DB table if not exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS echo_data (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# DB connection
def get_db_connection():
    return psycopg2.connect(
        host='db',
        database='echodb',
        user='postgres',
        password=os.getenv("POSTGRES_PASSWORD", "Pandu@2k3")
    )

# Reminder function
def speak_reminder(task_message):
    print("🚀 speak_reminder() called!")
    print(f"🔔 Reminder: {task_message}")
    if USE_TTS:
        engine.say(f"Reminder! {task_message}")
        engine.runAndWait()

@app.route('/')
def home():
    return "Echo App Running!"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    reminder_time = data.get('reminder_time')  # format: "HH:MM"

    if not name or not email or not message or not reminder_time:
        return jsonify({'error': 'Missing fields'}), 400

    try:
        # Parse reminder time
        now = datetime.now()
        remind_at = datetime.strptime(reminder_time, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if remind_at < now:
            remind_at += timedelta(days=1)

        # Save to DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO echo_data (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        cur.close()
        conn.close()

        # Schedule the task
        with scheduler_lock:
            scheduler.add_job(
                speak_reminder,
                'date',
                run_date=remind_at,
                args=[f"{name}, {message}"]
            )

        return jsonify({'message': 'Task scheduled successfully!'}), 200
    except Exception as e:
        logging.error(f"Error scheduling task: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5050)
