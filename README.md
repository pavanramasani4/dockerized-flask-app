# Dockerized Flask Web Application

## Overview

This project is a Flask web application that allows users to sign up, log in, and manage their sessions. It uses a SQLite database to store user information and implements secure password hashing. Dockerizing the application ensures consistent deployment across different environments and simplifies the setup process.

## Project Structure

```
dockerized-flask-app/
│
├── tests/
│   ├── __init__.py
│   └── test_Web.py
│
└── WebPage/
    ├── static/
    │   ├── home-styles.css
    │   ├── styles.css
    │   └── htmlcov/
    │       ├── index.html
    │       ├── coverage_html_*.js
    │       ├── style_*.css
    │       ├── *.png
    │       └── ... (other coverage report files)
    ├── templates/
    │   ├── home.html
    │   ├── index.html
    │   ├── login.html
    │   ├── signup.html
    │   └── users.html
    ├── Dockerfile
    ├── mydatabase.db
    ├── requirements.txt
    └── Week1.py
```

## Features

- User Registration and Authentication
- Session Management with Login and Logout
- Secure Password Storage using Hashing
- Flash Messages for User Feedback
- SQLite Database for User Data
- Unit Testing with Coverage Reports
- Dockerized for Consistent Deployment

## Prerequisites

- **Docker**: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).
- **Python 3.9+**: Required if running the application without Docker.

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/dockerized-flask-app.git
cd dockerized-flask-app
```

Replace `your-username` with your GitHub username.

### 2. Build the Docker Image

Build the Docker image using the provided `Dockerfile`.

```sh
docker build -t dockerized-flask-app .
```

### 3. Run the Docker Container

Run a container from the image you just built.

```sh
docker run -d -p 5000:5000 dockerized-flask-app
```

- `-d`: Runs the container in detached mode (in the background).
- `-p 5000:5000`: Maps port 5000 of the host to port 5000 of the container.
- `dockerized-flask-app`: The name of the image to run.

### 4. Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

You should see the application's home page.

## Generating and Viewing Test Coverage Reports

### Running Unit Tests with Coverage

To generate test coverage reports, follow these steps:

1. **Install Coverage.py**:

   If you're running the application locally (not within Docker), ensure you have `coverage` installed in your virtual environment:

   ```sh
   pip install coverage
   ```

2. **Run Tests with Coverage**:

   Navigate to the project directory and run:

   ```sh
   coverage run -m unittest discover -s tests
   ```

   This command discovers and runs all unit tests in the `tests` directory while collecting coverage data.

3. **Generate HTML Coverage Report**:

   After running the tests, generate the HTML report:

   ```sh
   coverage html
   ```

   This command creates an `htmlcov` directory containing the coverage report.

4. **Integrate Coverage Report into the Web Application**:

   Copy the `htmlcov` directory into the `static` folder of your Flask application:

   ```sh
   cp -r htmlcov/ WebPage/static/
   ```

   *(For Windows PowerShell, use the `Copy-Item` command as follows:)*

   ```powershell
   Copy-Item -Recurse -Path 'htmlcov' -Destination 'WebPage\static\htmlcov'
   ```

5. **Update `Week1.py` to Serve the Coverage Report**:

   Ensure your `Week1.py` file includes the following route:

   ```python
   @app.route('/coverage')
   def coverage_report():
       return redirect(url_for('static', filename='htmlcov/index.html'))
   ```

6. **Restart the Flask Application**:

   If the application is running, restart it to apply the changes:

   ```sh
   # If running locally
   python Week1.py

   # If running via Docker, rebuild the image and restart the container
   docker build -t dockerized-flask-app .
   docker stop <container_id>
   docker rm <container_id>
   docker run -d -p 5000:5000 dockerized-flask-app
   ```

7. **Access the Coverage Report**:

   Navigate to the coverage report in your web browser:

   ```
   http://localhost:5000/coverage
   ```

### Notes

- **Automating Coverage Report Updates**: For continuous integration, you may automate the generation and deployment of coverage reports.
- **Ensure Correct Paths**: By placing `htmlcov` inside the `static` folder, all static assets are correctly served by Flask.

## Project Details

### `Week1.py`

This is the main application file containing the Flask routes and application logic.

**Key Routes:**

- `/`: Home page (login form)
- `/signup`: Sign-up page
- `/submit_signup`: Handles sign-up form submission
- `/login`: Handles login form submission
- `/home`: User's home page after logging in
- `/logout`: Logs the user out
- `/coverage`: Displays the test coverage report

### Templates

- **index.html**: The login page template.
- **signup.html**: The sign-up page template.
- **home.html**: The user's home page template.
- **users.html**: Displays all users (for demonstration purposes).

### Static Files

- **styles.css**: Contains styling for the login and sign-up pages.
- **home-styles.css**: Contains styling for the home page.
- **htmlcov/**: Contains the HTML test coverage report.

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

## `requirements.txt`

Contains the Python dependencies for the application.

```text
Flask==2.0.2
Werkzeug==2.0.2
Jinja2==3.0.2
itsdangerous==2.0.1
click==8.0.3
coverage==7.6.1
unittest2==1.1.0
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
   docker rmi dockerized-flask-app
   ```

## Deploying on AWS EC2

### **Setup Instructions for AWS EC2**

#### **1. Launch an EC2 Instance**

1. Log in to your AWS Management Console.
2. Navigate to the EC2 Dashboard.
3. Click on "Launch Instance".
4. Choose an Amazon Machine Image (AMI) (e.g., Ubuntu Server 20.04 LTS).
5. Select an Instance Type (e.g., t2.micro for free tier eligibility).
6. Configure Instance Details and add Storage if needed.
7. Add Tags (optional).
8. Configure Security Group:
   - Allow SSH (port 22) from your IP.
   - Allow HTTP (port 80) from anywhere.
   - Allow Custom TCP Rule (port 5000) from anywhere.
9. Review and Launch the instance.
10. Download the key pair (.pem file) and keep it secure.

#### **2. Connect to Your EC2 Instance**

1. Open a terminal on your local machine.
2. Navigate to the directory where your key pair is stored.
3. Connect to your EC2 instance using SSH:

Of course, let's continue with the instructions for deploying the application on AWS EC2.

---

#### **3. Connect to Your EC2 Instance (cont.)**

3. Connect to your EC2 instance using SSH:

   ```sh
   ssh -i "your-key-pair.pem" ubuntu@your-ec2-public-dns
   ```

   - Replace `your-key-pair.pem` with the name of your key pair file.
   - Replace `your-ec2-public-dns` with the Public DNS of your EC2 instance, which can be found in the EC2 Dashboard.

#### **4. Update and Install Dependencies on the EC2 Instance**

Once connected to your EC2 instance, update the package list and install Docker:

```sh
sudo apt-get update
sudo apt-get install -y docker.io
```

#### **5. Clone the Repository on the EC2 Instance**

Clone your project repository on the EC2 instance:

```sh
git clone https://github.com/your-username/dockerized-flask-app.git
cd dockerized-flask-app
```

Replace `your-username` with your GitHub username.

#### **6. Build and Run the Docker Image on EC2**

Build the Docker image:

```sh
sudo docker build -t dockerized-flask-app .
```

Run the Docker container:

```sh
sudo docker run -d -p 5000:5000 dockerized-flask-app
```

#### **7. Access the Application**

Open your web browser and navigate to your EC2 instance's public DNS on port 5000:

```
http://your-ec2-public-dns:5000
```

You should see the application's home page.

### Notes

- **Ensure Security Group Rules**: Verify that the security group associated with your EC2 instance allows inbound traffic on port 5000 (as configured during instance launch).
- **Persistence of Data**: Since SQLite is used, data will be stored in the container. Consider using a persistent storage solution for production environments.
- **Automating Deployment**: For automated deployments, consider using AWS services like CodeDeploy or third-party tools like GitHub Actions or Jenkins.

---

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

---
