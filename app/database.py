import mysql.connector
from mysql.connector import Error

# FULL_DB_URL = "mysql://qwq44n23q3iz0jjj:miik1fpwkjr8qek9@tk3mehkfmmrhjg0b.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/vqh46dlxyis6rini"

HOST = 'tk3mehkfmmrhjg0b.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
DATABASE = 'vqh46dlxyis6rini'
USER = 'qwq44n23q3iz0jjj'
PASSWORD = 'miik1fpwkjr8qek9'


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def create_test_connection():
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
