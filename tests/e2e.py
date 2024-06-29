import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import create_connection

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    connection = create_connection()
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
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    response = client.post("/users/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login():
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert data["username"] == "testuser"


def test_create_operation():
    response = client.post("/operations/", json={"type": "addition", "cost": 1.0})
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "addition"
    assert data["cost"] == 1.0
    assert "id" in data


def test_calculate():
    response = client.post("/operations/", json={"type": "addition", "cost": 1.0})
    assert response.status_code == 200
    operation_id = response.json()["id"]
    client.post("/users/", json={"username": "testuser", "password": "testpassword"})
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    token = response.json()["username"]

    response = client.post(
        "/calculate/",
        json={"operation_id": operation_id, "user": {'hello': 1}},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "operation_response" in data
    assert data["operation_response"] == "2"
