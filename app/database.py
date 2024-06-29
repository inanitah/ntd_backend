import mysql.connector
from mysql.connector import Error


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='calculator',
            user='calculator_user',
            password='password'
        )
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
