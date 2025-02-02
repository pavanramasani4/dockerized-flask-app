# Dockerized-Flask-App

## Overview

This project is a Flask web application that allows users to sign up, log in, and manage their sessions. It uses a SQLite database to store user information and implements secure password hashing. The application is Dockerized for easy deployment and consistency across environments.

## Project Structure

```plaintext
MyProjectGroup/
│
├── static/
│   ├── home-styles.css
│   └── styles.css
├── templates/
│   ├── home.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── user.html
├── Dockerfile
├── requirements.txt
└── Week1.py

Features
 └── User Registration and Authentication
 └── Session Management with Login and Logout
 └── Secure Password Storage using Hashing
 └── Flash Messages for User Feedback
 └── SQLite Database for User Data
 └── Dockerized for Consistent Deployment

Prerequisites
 └── Python 3.9 or higher
 └── Docker (optional, for Dockerized deployment)

Installation
Follow these steps to set up and run the application locally without Docker.

1. Clone the Repository

git clone https://github.com/your-username/my-flask-app.git  ----#Replace "your-username" with your GitHub username.
cd my-flask-app

2. Create and Activate a Virtual Environment

python -m venv venv  #For Windows
(Or)
venv\Scripts\activate #For macOS/Linux:

source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Up the Database
The application uses SQLite. The database will be created automatically when you run the app for the first time.

5. Run the Application
python Week1.py  #The application will start running on http://localhost:5000.

Running the Application 
Open your web browser and navigate to http://localhost:5000 to access the application.

Docker Deployment
Deploying the application with Docker ensures consistency across different environments.

1. Build the Docker Image
docker build -t my-flask-app .

2. Run the Docker Container
docker run -d -p 5000:5000 my-flask-app  #The -d flag runs the container in detached mode.

The -p 5000:5000 option maps port 5000 on your local machine to port 5000 in the container.

3. Access the Application
Open your web browser and navigate to http://localhost:5000.
