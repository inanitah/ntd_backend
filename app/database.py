import mysql.connector
from mysql.connector import Error, pooling
from fastapi import Request, Response
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
        pool_size=int(os.getenv('DB_POOL_SIZE', 5)),  # Default pool size is 5 if not specified
        **dbconfig
    )
    print("Connection pool created successfully")
except Error as e:
    print(f"Error creating connection pool: {e}")


# Function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(**dbconfig)
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"The error '{e}' occurred")
    return None


# Middleware to handle database connections
async def db_session_middleware(request: Request, call_next):
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
