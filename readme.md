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
- POST /api/v1/token: Authenticate user and get a token
- POST /api/v1/users/: Create a new user
- GET /api/v1/operations/: Retrieve all operations
- POST /api/v1/operations/: Create a new operation
- POST /api/v1/calculate/: Perform a calculation
- DELETE /api/v1/records/{id}: Soft delete a record
- GET /api/v1/records/: Retrieve user records

## Setup Instructions

### 1. Clone the Repository
```bash
git clone git@github.com:inanitah/ntd_backend.git
cd <repository-directory>/ntd_backend
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```


### 4. Initialize the MySQL Database
```sql
CREATE DATABASE calculator;
CREATE USER 'calculator_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON calculator.* TO 'calculator_user'@'localhost';
FLUSH PRIVILEGES;
```


### 5. Run the script to create the tables
```bash
python create_tables.py
```

### 6. Run the FastAPI server
```bash
uvicorn app.main:app --reload
```

### Running tests

### 1. Setup the MySQL Database
```sql
CREATE DATABASE calculator_test;
CREATE USER 'calculator_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON calculator_test.* TO 'calculator_user'@'localhost';
FLUSH PRIVILEGES;
```


### 2. Running the tests
```bash
pytest test_calculator.py
```

### Deployment

### 1. Login to heroku
```bash
heroku login
```


### 2. Set the Remote Heroku Existing App
```bash
heroku git:remote -a ntdbackend
```


### 3. Deploy the backend
```bash
git push heroku main
```

### API Documentation

Production url to perform the api calls:
https://ntdbackend-3703dd1358c1.herokuapp.com
User and password available for the example: {username: 1, password: 1}

- User Registration
- Endpoint: /api/v1/users/
- Method: POST
- Request Body:
```json
{
    "username": "1",
    "password": "1"
}
```
- Response:
```json
{
    "id": 1,
    "username": "1",
    "balance": 100.0,
    "status": "active"
}
```
User Login
- Endpoint: /api/v1/token
- Method: POST
- Request Body:
```application/x-www-form-urlencoded
{
    "username": "1",
    "password": "1"
}
```
- Response:
```json
{
    "username": "1"
}
```

Create Operation
- Endpoint: /api/v1/operations/
- Method: POST
- Request Body:
```json
{
    "type": "addition",
    "cost": 1.0
}
```
- Response:
```json
{
    "id": 1,
    "type": "addition",
    "cost": 1.0
}
```
- Headers:
```plaintext
    Authorization: Bearer <token>
```
Perform Calculation
- Endpoint: /api/v1/calculate/
- Method: POST
- Request Body:
```json
{
    "operation_id": 1
}
```
- Response:
```json
{
    "id": 1,
    "operation_id": 1,
    "user_id": 1,
    "amount": 1.0,
    "user_balance": 99.0,
    "operation_response": "2",
    "created_at": "2024-06-30T21:57:47",
    "deleted": false
}
```
- Headers:
```plaintext
    Authorization: Bearer <token>
```
Get Operations
- Endpoint: /api/v1/operations/
- Method: GET
- Response:
```json
[
    {
        "id": 1,
        "type": "addition",
        "cost": 1.0
    }
]
```
- Headers:
```plaintext
    Authorization: Bearer <token>
```
Get User Records
- Endpoint: /api/v1/records/
- Method: GET
- Query Parameters:
- -`search` (optional): Filter records by partial matches.
- - `skip` (optional): Number of records to skip for pagination.
- - `limit` (optional): Maximum number of records to return.
- Response:
```json
[
    {
        "id": 1,
        "operation_id": 1,
        "user_id": 1,
        "amount": 1.0,
        "user_balance": 99.0,
        "operation_response": "2",
        "created_at": "2024-06-30T21:57:47",
        "deleted": false
    }
]
```
- Headers:
```plaintext
    Authorization: Bearer <token>
```
Delete Record (Soft Delete)
- Endpoint: /api/v1/records/{id}
- Method: DELETE
- Response:
```json
{
    "id": 1,
    "operation_id": 1,
    "user_id": 1,
    "amount": 1.0,
    "user_balance": 99.0,
    "operation_response": "2",
    "created_at": "2024-06-30T21:57:47",
    "deleted": true
}
```
- Headers:
```plaintext
    Authorization: Bearer <token>
```

### Note that the token value is obtained from the response of the token endpoint and is provided in the username field.