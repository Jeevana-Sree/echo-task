from flask import Flask, request, jsonify, render_template
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from threading import Lock
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Global scheduler
scheduler = BackgroundScheduler()
scheduler.start()
scheduler_lock = Lock()

# DB connection
def get_db_connection():
    return psycopg2.connect(
        host='db',
        database='echodb',
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )

@app.route('/')
def home():
    return render_template('index.html')  # serve web UI

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    reminder_time = data.get('reminder_time')  # format: "HH:MM"

    if not name or not email or not message or not reminder_time:
        return jsonify({'error': 'Missing fields'}), 400

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

    # Schedule task
    try:
        remind_at = datetime.strptime(reminder_time, "%H:%M").replace(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )

        with scheduler_lock:
            scheduler.add_job(
                lambda: print(f"🔔 Reminder: {name}, {message}"),
                'date',
                run_date=remind_at
            )

        return jsonify({'message': 'Task scheduled successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
