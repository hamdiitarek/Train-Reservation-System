import mysql.connector

def ConnectToDatabase():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        print("Connected To Database")
        return connection
    except mysql.connector.Error as Error:
        print("Failed to Connect to Database")
        return None
    
def Create_Database(connection, database_name):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
        print("Database '{}' Created Successfully".format(database_name))
    except mysql.connector.Error as Error:
        print("Failed to Create Database:", Error)

connection = ConnectToDatabase()

Create_Database(connection, "Reserve")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Reserve"
)