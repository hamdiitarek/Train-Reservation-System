import mysql.connector

def ConnectToDatabase(host="localhost", port="3308", user="root", password="Admin@123", database="Reserve"):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("Connected To Database \"{}\"".format(connection.database))
        return connection
    except mysql.connector.Error as error:
        print("Failed to Connect to Database {}".format(database))
        try:
            # Try to create the database
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database))
            print("Database '{}' Created Successfully".format(database))
            cursor.close()
            # Reconnect after creating the database
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
        except mysql.connector.Error as error:
            print("Failed to create Database:", error)
            return None
        return None
    
def Create_Database(connection, database_name):
        try:
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
            print("Database '{}' Created Successfully".format(database_name))
        except mysql.connector.Error as Error:
            print("Failed to Create Database:", Error)
            

# connection = mysql.connector.connect(
#     host="localhost:3308",
#     user="root",
#     port="3308",
#     password="Admin@123",
#     database="Reserve"
# )

connection = ConnectToDatabase()




