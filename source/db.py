import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")

def connect():
    conn = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

def query_by_slack_id(slack_id):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE slack_id = %s", (slack_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def add_user(name= None, slack_id=None, email= None, coding_time=0, api_key=None, roblox_user=None, bobux_balance=0 ):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (name, slack_id, coding_time, email_address, api_key, roblox_user, bobux_balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, slack_id, coding_time, email, api_key, roblox_user, bobux_balance))
    conn.commit()
    conn.close()

conn = connect()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slack_uid VARCHAR(64) UNIQUE NOT NULL,
    coding_time INT DEFAULT 0,
    email_address VARCHAR(255),
    api_key VARCHAR(255),
    roblox_user VARCHAR(255),
    bobux_balance INT DEFAULT 0
);
""")

conn.commit()
conn.close()
