from app.consts import Status
from app import schemas
from mysql.connector import MySQLConnection


def get_user_by_username(connection: MySQLConnection, username: str) -> dict:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()


def create_user(connection: MySQLConnection, user: schemas.UserCreate, hashed_password: str, status: Status) -> dict:
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, hashed_password, status) VALUES (%s, %s, %s)",
        (user.username, hashed_password, status.value)
    )
    connection.commit()
    return get_user_by_username(connection, user.username)


def get_operations(connection: MySQLConnection, skip: int = 0, limit: int = 10) -> list:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM operations LIMIT %s OFFSET %s", (limit, skip))
    return cursor.fetchall()


def create_operation(connection: MySQLConnection, operation: schemas.OperationCreate) -> int:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO operations (type, cost) VALUES (%s, %s)", (operation.type, operation.cost))
    connection.commit()
    return cursor.lastrowid


def create_record(connection: MySQLConnection, record: schemas.RecordCreate) -> int:
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO records (operation_id, user_id, amount,"
        " user_balance, operation_response) VALUES (%s, %s, %s, %s, %s)",
        (record.operation_id, record.user_id, record.amount, record.user_balance, record.operation_response)
    )
    connection.commit()
    return cursor.lastrowid


def get_record(connection: MySQLConnection, record_id: int) -> dict:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM records WHERE id = %s", (record_id,))
    return cursor.fetchone()


def get_records(
    connection: MySQLConnection, skip: int = 0, limit: int = 10, search: str = None, user_id: int = None
) -> list:
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT id, operation_id, user_id, amount, user_balance, operation_response, created_at, deleted 
    FROM records 
    WHERE user_id = %s AND deleted = FALSE
    """
    params = [user_id]

    if search:
        search_query = """
        AND (
            operation_response LIKE %s OR
            CAST(operation_id AS CHAR) LIKE %s OR
            CAST(user_id AS CHAR) LIKE %s OR
            CAST(amount AS CHAR) LIKE %s OR
            CAST(user_balance AS CHAR) LIKE %s OR
            created_at LIKE %s
        )
        """
        search_param = f"%{search}%"
        params.extend([search_param] * 6)
        query += search_query

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, skip])
    cursor.execute(query, tuple(params))
    return cursor.fetchall()


def soft_delete_record(connection: MySQLConnection, record_id: int) -> dict:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("UPDATE records SET deleted = TRUE WHERE id = %s", (record_id,))
    connection.commit()
    cursor.execute("SELECT * FROM records WHERE id = %s", (record_id,))
    return cursor.fetchone()


def update_user_balance(connection: MySQLConnection, user_id: int, new_balance: float) -> None:
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (new_balance, user_id))
    connection.commit()
