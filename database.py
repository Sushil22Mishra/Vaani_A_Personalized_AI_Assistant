import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Change if needed
        password="system",  # Change to your MySQL password
        database="voice_assistant"
    )
