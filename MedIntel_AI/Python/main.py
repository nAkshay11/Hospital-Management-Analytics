from database_connection import get_connection

connection = get_connection()

if connection:
    print("Database is Ready 🚀")
    connection.close()