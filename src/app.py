import os
import sqlite3
import json
from dotenv import load_dotenv
from threading import Thread
from flask import Flask, request, redirect, url_for, session

from app.auth import AUTH_URL, get_token
from app.main_loop import main_loop
from db.database import init_db
from utils.utils import generate_random_string

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

app = Flask(__name__)
app.secret_key = generate_random_string()
app.config['SESSION_COOKIE_NAME'] = generate_random_string()

is_running = False      # bool variable to avoid relaunching the main loop if it is already running

@app.get('/')
def authorize():
    return redirect(AUTH_URL)

@app.get('/redirect')
def redirectPage():
    if not request.args.get('code'):
        return redirect(AUTH_URL)
    
    code = request.args.get('code')
    session['tokens'] = get_token(code)
    session['refresh_token'] = session['tokens']['refresh_token']
    init_db()
    return redirect(url_for('run_loop'))

@app.get('/run')
def run_loop():
    if not session:
        return redirect(AUTH_URL)
    
    global is_running
    if not is_running:
        thread = Thread(target=main_loop, args=(session['tokens'],session['refresh_token']))
        thread.daemon = True
        thread.start()
        is_running = thread.is_alive()
    return f"The script is running properly. Please use the <a href=/get_history>/get_history</a> endpoint to retrieve your Spotify playing history."

@app.get('/get_history')
def get_history():
    if not session:
        return redirect(AUTH_URL)
    
    start = request.args.get('start') or '1000-01-01'
    end = request.args.get('end') or '4000-01-01'

    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row      # to get a more readble JSON response in the end
    cur = conn.cursor()
    rows = cur.execute(f"SELECT * FROM playing_history WHERE started_at BETWEEN '{start}' AND '{end} 23:59';").fetchall()
    conn.close()
    results = [dict(row) for row in rows]
    json_results = json.dumps(results,ensure_ascii=False)

    if json_results == '[]':
        return 'No data is available yet.'
    return json_results


app.run(host=HOST, port=PORT)
