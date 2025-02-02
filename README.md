Sure! Here's a complete `README.md` file tailored for your Dockerized Flask web application:

# Dockerized Flask Web Application

## Overview

This project is a Flask web application that allows users to sign up, log in, and manage their sessions. It uses a SQLite database to store user information and implements secure password hashing. Dockerizing the application ensures consistent deployment across different environments and simplifies the setup process.

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
```

## Features

- User Registration and Authentication
- Session Management with Login and Logout
- Secure Password Storage using Hashing
- Flash Messages for User Feedback
- SQLite Database for User Data
- Dockerized for Consistent Deployment

## Prerequisites

- Docker: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/Dockerized-Flask-Appgit
cd Dockerized-Flask-App
```

Replace `your-username` with your GitHub username.

### 2. Build the Docker Image

Build the Docker image using the provided `Dockerfile`.

```sh
docker build -t Dockerized-Flask-App.
```

### 3. Run the Docker Container

Run a container from the image you just built.

```sh
docker run -d -p 5000:5000 Dockerized-Flask-App
```

- `-d`: Runs the container in detached mode (in the background).
- `-p 5000:5000`: Maps port 5000 of the host to port 5000 of the container.
- `Dockerized-Flask-App`: The name of the image to run.

### 4. Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

You should see the application's home page.

## Project Details

### Week1.py

This is the main application file containing the Flask routes and application logic.

**Key Routes:**

- `/`: Home page (login form)
- `/signup`: Sign-up page
- `/submit_signup`: Handles sign-up form submission
- `/login`: Handles login form submission
- `/home`: User's home page after logging in
- `/logout`: Logs the user out

### Templates

- **index.html**: The login page template.
- **signup.html**: The sign-up page template.
- **home.html**: The user's home page template.
- **user.html**: Displays all users (for demonstration purposes).

### Static Files

- **styles.css**: Contains styling for the login and sign-up pages.
- **home-styles.css**: Contains styling for the home page.

### Database

- **SQLite**: The application uses SQLite for simplicity. The database file `mydatabase.db` is created automatically.

## Dockerfile

The `Dockerfile` contains the instructions to build the Docker image for the Flask application.

```Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=Week1.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
```

## Requirements.txt

Contains the Python dependencies for the application.

```text
Flask==2.0.2
Werkzeug==2.0.2
Jinja2==3.0.2
itsdangerous==2.0.1
click==8.0.3
```

Add any additional dependencies your application requires.

## Logging

Logs from the Flask application can be viewed using:

```sh
docker logs <container_id>
```

To get the `<container_id>`, run:

```sh
docker ps
```

## Stopping the Application

To stop the running container:

1. List running containers:

   ```sh
   docker ps
   ```

2. Stop the container:

   ```sh
   docker stop <container_id>
   ```

## Cleaning Up

To remove the Docker image and container:

1. Stop and remove the container:

   ```sh
   docker stop <container_id>
   docker rm <container_id>
   ```

2. Remove the image:

   ```sh
   docker rmi my-flask-app
   ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.

   ```sh
   git checkout -b feature/your-feature-name
   ```

3. Commit your changes.

   ```sh
   git commit -am 'Add new feature'
   ```

4. Push to the branch.
   
   ```sh
   git push origin feature/your-feature-name
   ```
5. Open a pull request.
