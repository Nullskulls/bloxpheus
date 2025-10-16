import os, secrets
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
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


def update_email(slack_id, email):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email_address = %s WHERE slack_id = %s", (email, slack_id))
    conn.commit()
    conn.close()

def update_api_key(slack_id, api_key):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET api_key = %s WHERE slack_id = %s", (api_key, slack_id))
    conn.commit()
    conn.close()

def remove_roblox_account(slack_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET roblox_user = NULL where slack_id = %s", (slack_id,))
    conn.commit()
    conn.close()
def update_balance(slack_id, balance):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET bobux_balance = %s where slack_id = %s", (balance, slack_id))
    conn.commit()
    conn.close()

def add_verification_request(roblox_user, slack_id):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM request_logs WHERE slack_id = %s", (slack_id,))
    data = cursor.fetchone()
    temp_code = ''.join(secrets.choice('0123456789') for _ in range(12))
    if not data:
        cursor.execute("INSERT INTO request_logs (request_time, slack_id, roblox_user, verification_code) VALUES (%s, %s, %s, %s)", (datetime.now(), slack_id, roblox_user, temp_code))
    else:
        req_time = data["request_time"]
        req_time = req_time.replace(tzinfo=timezone.utc)
        if (datetime.now(timezone.utc) - req_time) > timedelta(minutes=30):
            cursor.execute("UPDATE request_logs SET verification_code = %s, request_time = NOW() WHERE slack_id = %s",(temp_code, slack_id))
        else:
            conn.close()
            return None
    conn.commit()
    conn.close()
    return temp_code

def get_verification_data(slack_id):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM request_logs WHERE slack_id = %s", (slack_id,))
    data = cursor.fetchone()
    conn.close()
    return data

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS request_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    slack_id VARCHAR(64) NOT NULL,
    roblox_user VARCHAR(255),
    verification_code VARCHAR(32)
);
""")
conn.commit()
conn.close()
