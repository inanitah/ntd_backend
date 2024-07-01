# Arithmetic Calculator REST API Backend

This project provides a RESTful API for a simple arithmetic calculator with user authentication and balance management.
The API supports basic operations such as addition, subtraction, multiplication, division, square root, and random string generation.
Each operation has an associated cost that deducts from the user's balance.

## Tech Stack
- Backend: Python, FastAPI
- Database: MySQL
- Deployment: Heroku

## Features
- User registration and authentication
- Arithmetic operations with cost per request
- Random string generation
- User balance management
- Operation records with soft delete functionality

## Prerequisites
- Python 3.8+
- MySQL
- Heroku CLI (for deployment)

## API Endpoints:
API Endpoints
POST /api/v1/token: Authenticate user and get a token
POST /api/v1/users/: Create a new user
GET /api/v1/operations/: Retrieve all operations
POST /api/v1/operations/: Create a new operation
POST /api/v1/calculate/: Perform a calculation
DELETE /api/v1/records/{id}: Soft delete a record
GET /api/v1/records/: Retrieve user records

## Setup Instructions

### 1. Clone the Repository
git clone git@github.com:inanitah/ntd_backend.git
cd <repository-directory>/ntd_backend


### 2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate


### 3. Install requirements
pip install -r requirements.txt


### 4. Initialize the MySQL Database
CREATE DATABASE calculator;
CREATE USER 'calculator_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON calculator.* TO 'calculator_user'@'localhost';
FLUSH PRIVILEGES;


### 5. Run the script to create the tables
python create_tables.py


### 6. Run the FastAPI server
uvicorn app.main:app --reload



Running tests

### 1. Setup the MySQL Database
CREATE DATABASE calculator_test;
CREATE USER 'calculator_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON calculator_test.* TO 'calculator_user'@'localhost';
FLUSH PRIVILEGES;


### 2. Running the tests
pytest test_calculator.py


Deployment

### 1. Login to heroku
heroku login


### 2. Set the Remote Heroku Existing App
heroku git:remote -a ntdbackend


### 3. Deploy the backend
git push heroku main





