import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="library"
        )
        if conn.is_connected():
            print("✅ MySQL Connection Successful")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
        return None

# Test the connection
conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    print(cursor.fetchall())
    conn.close()
