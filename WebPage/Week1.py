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
        g.db = sqlite3.connect('/app/WebPage/mydatabase.db')
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
        conn.execute('INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)',
                     (first_name, last_name, create_username, hashed_password))
        conn.commit()
        flash("Account created successfully! Please log in.", 'success')
        return redirect(url_for('login'))
    return redirect(url_for('signup'))

# Route for login page and handling login form submission
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']  # Store username in session
            session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Record session start time

            # Update session_start in database
            conn.execute('UPDATE users SET session_start = ? WHERE username = ?', (session['start_time'], username))
            conn.commit()

            return redirect(url_for('homepage'))  # Redirect to homepage on successful login
        else:
            flash("Invalid username or password.", 'error')  # Flash error message
            return render_template('login.html')  # Render login.html on error
    return render_template('login.html')  # Render login form on GET request

# Route for displaying all users (for demonstration purposes)
@app.route("/users")
def display_users():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    return render_template('users.html', users=users)  # Render users.html template with user data

# Route for the homepage
@app.route("/home")
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('home.html', username=session.get('username'))  # Use .get() to avoid KeyError

# Route for logging out
@app.route("/logout", methods=["POST"])
def logout():
    username = session.get('username')
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Record session end time

    # Update session_end in database
    conn = get_db_connection()
    conn.execute('UPDATE users SET session_end = ? WHERE username = ?', (end_time, username))
    conn.commit()

    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home'))  # Redirect to home page

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Bind to 0.0.0.0 to accept connections from any IP
