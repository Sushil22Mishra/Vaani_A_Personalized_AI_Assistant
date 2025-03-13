import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Ensure this is 'root'
        password="system",    # Ensure this matches the password you set
        database="vaani_database",
        auth_plugin='mysql_native_password'  # Specify the authentication plugin
    )

def insert_user(name, password, profile_pic):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, password, profile_pic) VALUES (%s, %s, %s)",
            (name, password, profile_pic)
        )
        connection.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

def get_user_by_name(name):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for easier access
    try:
        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        user = cursor.fetchone()  # Fetch a single user record
        return user  # Return the user record as a dictionary
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()
