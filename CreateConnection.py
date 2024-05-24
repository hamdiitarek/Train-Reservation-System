import mysql.connector as sql
import os
from dotenv import load_dotenv

load_dotenv(os.path.dirname(__file__))

def create():
    
    host = os.getenv("host")
    port = os.getenv("port")
    user = os.getenv("user")
    password = os.getenv("password")
    database = os.getenv("database")

    connection = sql.connect(host=host, port=port, user=user, password=password)

    backEnd = connection.cursor()
    backEnd.execute("CREATE DATABASE IF NOT EXISTS {}".format(database))
    backEnd.close()

    connection.close()
    connection = sql.connect(
        host=host, port=port, user=user, password=password, database=database
    )
    return connection
