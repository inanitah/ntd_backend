from app.database import create_connection
from app import schemas

connection = create_connection()


def get_user(user_id: int):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()


def get_user_by_username(username: str) -> dict:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()


def create_user(user: schemas.UserCreate, hashed_password: str) -> dict:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, hashed_password) VALUES (%s, %s)", (user.username, hashed_password))
    connection.commit()
    return get_user_by_username(user.username)


def get_operations(skip: int = 0, limit: int = 10):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM operations LIMIT %s OFFSET %s", (limit, skip))
    return cursor.fetchall()


def create_operation(operation: schemas.OperationCreate) -> str:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO operations (type, cost) VALUES (%s, %s)", (operation.type, operation.cost))
    connection.commit()
    return cursor.lastrowid


def create_record(record: schemas.RecordCreate) -> str:
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO records (operation_id, user_id, amount,"
        " user_balance, operation_response) VALUES (%s, %s, %s, %s, %s)",
        (record.operation_id, record.user_id, record.amount, record.user_balance, record.operation_response)
    )
    connection.commit()
    return cursor.lastrowid


def get_record(record_id: int):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM records WHERE id = %s", (record_id,))
    return cursor.fetchone()
