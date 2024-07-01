import pytest
import mysql.connector
from mysql.connector import Error
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

# Set environment variables for the test database
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'calculator_test'
os.environ['DB_USER'] = 'calculator_user'
os.environ['DB_PASSWORD'] = 'password'
os.environ['DB_POOL_SIZE'] = '5'


def create_test_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    connection = create_test_connection()
    cursor = connection.cursor()

    # Drop foreign keys first
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS records")
    cursor.execute("DROP TABLE IF EXISTS operations")
    cursor.execute("DROP TABLE IF EXISTS users")

    # Create tables
    cursor.execute("""
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        hashed_password VARCHAR(255),
        balance FLOAT DEFAULT 100.0,
        status VARCHAR(255) DEFAULT 'active'
    )
    """)

    cursor.execute("""
    CREATE TABLE operations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(255),
        cost FLOAT
    )
    """)

    cursor.execute("""
    CREATE TABLE records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        operation_id INT,
        user_id INT,
        amount FLOAT,
        user_balance FLOAT,
        operation_response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deleted BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (operation_id) REFERENCES operations(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    connection.commit()

    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")

    yield

    # Teardown: Clean up after tests
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    cursor.execute("DROP TABLE IF EXISTS records")
    cursor.execute("DROP TABLE IF EXISTS operations")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")

    connection.commit()
    connection.close()


def test_create_user():
    response = client.post("/api/v1/users/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login():
    response = client.post("/api/v1/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert data["username"] == "testuser"


def test_create_operation():
    response = client.post("/api/v1/operations/", json={"type": "addition", "cost": 1.0})
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "addition"
    assert data["cost"] == 1.0
    assert "id" in data


def test_calculate():
    response = client.post("/api/v1/operations/", json={"type": "addition", "cost": 1.0})
    assert response.status_code == 200
    operation_id = response.json()["id"]
    client.post("/api/v1/users/", json={"username": "testuser", "password": "testpassword"})
    response = client.post("/api/v1/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    token = response.json()["username"]

    response = client.post(
        "/api/v1/calculate/",
        json={"operation_id": operation_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "operation_response" in data
    assert data["operation_response"] == "2"


def test_soft_delete_record():
    response = client.post("/api/v1/operations/", json={"type": "addition", "cost": 1.0})
    assert response.status_code == 200
    operation_id = response.json()["id"]
    client.post("/api/v1/users/", json={"username": "testuser", "password": "testpassword"})
    response = client.post("/api/v1/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    token = response.json()["username"]

    response = client.post(
        "/api/v1/calculate/",
        json={"operation_id": operation_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    record_id = response.json()["id"]

    # Soft delete the record
    response = client.delete(f"/api/v1/records/{record_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Verify the record is soft deleted
    response = client.get("/api/v1/records/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    records = response.json()
    for record in records:
        assert record["id"] != record_id  # Ensure the soft deleted record is not returned
