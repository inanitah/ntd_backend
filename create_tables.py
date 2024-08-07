from app.database import create_connection

connection = create_connection()

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT, 
    username VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255),
    balance FLOAT DEFAULT 100.0,
    status VARCHAR(255) DEFAULT 'active',
    PRIMARY KEY (id)
)
"""

create_operations_table = """
CREATE TABLE IF NOT EXISTS operations (
    id INT AUTO_INCREMENT, 
    type VARCHAR(255), 
    cost FLOAT,
    PRIMARY KEY (id)
)
"""

create_records_table = """
CREATE TABLE IF NOT EXISTS records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operation_id INT,
    user_id INT,
    amount DECIMAL(10, 2),
    user_balance DECIMAL(10, 2),
    operation_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (operation_id) REFERENCES operations(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

cursor = connection.cursor()
cursor.execute(create_users_table)
cursor.execute(create_operations_table)
cursor.execute(create_records_table)

print("Tables created successfully!")

