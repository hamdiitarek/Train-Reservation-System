import mysql.connector as sql
import os
from dotenv import load_dotenv

load_dotenv(os.path.dirname(__file__))

host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")

def connect():
    return sql.connect(
        host=host, port=port, user=user, password=password, database=database
    )


def create():
    # First, connect to MySQL without specifying a database
    connection = sql.connect(host=host, port=port, user=user, password=password)

    backEnd = connection.cursor()

    # Create the database
    backEnd.execute("CREATE DATABASE IF NOT EXISTS reserve")

    # Close the initial connection
    backEnd.close()
    connection.close()

    # Now, connect to the newly created database
    connection = sql.connect(host=host, port=port, user=user, password=password, database=database)

    return connection

