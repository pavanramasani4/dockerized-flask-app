from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a random secret key for session management

# Function to connect to the SQLite database
def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect('WebPage/mydatabase.db')
        g.db.row_factory = sqlite3.Row
        with g.db:
            g.db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    session_start TEXT,
                    session_end TEXT
                )
            ''')
            g.db.commit()
            print("Table 'users' created or already exists.")
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Route for the home page
@app.route("/")
def home():
    return render_template('index.html')  # Render index.html template

# Route for the signup page
@app.route("/signup")
def signup():
    return render_template('signup.html')  # Render signup.html template

# Route for handling signup form submission
@app.route("/submit_signup", methods=["POST"])
def submit_signup():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        create_username = request.form.get('create_username')
        create_password = request.form.get('create_password')

        # Basic form validation
        if not first_name or not last_name or not create_username or not create_password:
            flash("All fields are required.", 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(create_password)  # Hash the password

        conn = get_db_connection()
        # Check if the username already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (create_username,)).fetchone()

        if existing_user:
            flash("Username already exists. Please choose a different one.", 'error')
            return redirect(url_for('signup'))

        # Insert new user into the database
        conn.execute('INSERT INTO users (first
