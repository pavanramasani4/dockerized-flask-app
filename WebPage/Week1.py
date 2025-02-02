from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# Initialize Flask application
webpage = Flask(__name__)
webpage.secret_key = 'your_secret_key'  # VERY IMPORTANT: Set a random secret key for session management

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    with conn:  # Use context manager for initial table creation
        conn.execute('''
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
        conn.commit()
    return conn  # Return the same connection object

# Route for the home page
@webpage.route("/")
def home():
    return render_template('index.html')  # Render index.html template

# Route for the signup page
@webpage.route("/signup")
def signup():
    return render_template('signup.html')  # Render signup.html template

# Route for handling signup form submission
@webpage.route("/submit_signup", methods=["POST"])
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

        with get_db_connection() as conn:
            # Check if the username already exists
            existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (create_username,)).fetchone()

            if existing_user:
                flash("Username already exists. Please choose a different one.", 'error')
                return redirect(url_for('signup'))

            # Insert new user into the database
            conn.execute('INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)',
                         (first_name, last_name, create_username, hashed_password))
            conn.commit()
            flash("Account created successfully! Please log in.", 'success')
            return redirect(url_for('login'))
    return redirect(url_for('signup'))

# Route for login page and handling login form submission
@webpage.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']  # Store username in session
            session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Record session start time

            # Update session_start in database
            with get_db_connection() as conn:
                conn.execute('UPDATE users SET session_start = ? WHERE username = ?', (session['start_time'], username))
                conn.commit()
            
            return redirect(url_for('homepage'))  # Redirect to homepage on successful login
        else:
            flash("Invalid username or password.", 'error')  # Flash error message
            return render_template('login.html')  # Render login.html on error
    return render_template('login.html')  # Render login form on GET request

# Route for displaying all users (for demonstration purposes)
@webpage.route("/users")
def display_users():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    with get_db_connection() as conn:
        users = conn.execute('SELECT * FROM users').fetchall()
    return render_template('users.html', users=users)  # Render users.html template with user data

# Route for the homepage
@webpage.route("/home")
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('home.html', username=session.get('username'))  # Use .get() to avoid KeyError

# Route for logging out
@webpage.route("/logout", methods=["POST"])
def logout():
    username = session.get('username')
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Record session end time

    # Update session_end in database
    with get_db_connection() as conn:
        conn.execute('UPDATE users SET session_end = ? WHERE username = ?', (end_time, username))
        conn.commit()

    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home'))  # Redirect to home page

# Run the Flask application
if __name__ == '__main__':
    webpage.run(debug=True)  # Run the app in debug mode
