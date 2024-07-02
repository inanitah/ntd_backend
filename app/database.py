import mysql.connector
from mysql.connector import Error
from fastapi import Request, Response
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Function to create a database connection
def create_connection():
    try:
        dbconfig = dict(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        connection = mysql.connector.connect(**dbconfig)
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"The error '{e}' occurred")
    return None


# Middleware to handle database connections
async def db_session_middleware(request: Request, call_next):
    # Database configuration
    dbconfig = dict(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

    # Create a connection pool
    try:
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=int(os.getenv('DB_POOL_SIZE', 5)),
            **dbconfig
        )
        print("Connection pool created successfully")
    except Error as e:
        print(f"Error creating connection pool: {e}")
        raise
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = connection_pool.get_connection()
        if request.state.db and request.state.db.is_connected():
            response = await call_next(request)
        else:
            response = Response("Database connection failed", status_code=500)
    except Exception as e:
        print(f"Error during request processing: {e}")
    finally:
        if request.state.db and request.state.db.is_connected():
            request.state.db.close()
    return response


def drop_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (os.getenv('DB_NAME'),))
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    connection.commit()
