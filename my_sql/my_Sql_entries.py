import mysql.connector

def check_and_create_table(connection, table_name, create_table_sql):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        if result:
            print(f"Table '{table_name}' already exists.")
        else:
            cursor.execute(create_table_sql)
            print(f"Table '{table_name}' created successfully.")
    except mysql.connector.Error as error:
        print(f"Error checking/creating table '{table_name}':", error)
    finally:
        cursor.close()

def create_index_if_not_exists(connection, table_name, index_name, create_index_sql):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SHOW INDEX FROM {table_name} WHERE Key_name = '{index_name}'")
        result = cursor.fetchone()
        if result:
            print(f"Index '{index_name}' on table '{table_name}' already exists.")
        else:
            cursor.execute(create_index_sql)
            print(f"Index '{index_name}' on table '{table_name}' created successfully.")
    except mysql.connector.Error as error:
        print(f"Error checking/creating index '{index_name}' on table '{table_name}':", error)
    finally:
        cursor.close()

def Construct_Database(connection):
    if connection:
        create_Coach_table_sql = """
            CREATE TABLE Coach (
                Train_ID NUMERIC(10),
                Coach_Number NUMERIC(4),
                Number_Seats NUMERIC,
                Max_Seats NUMERIC,
                Class VARCHAR(15),
                PRIMARY KEY(Train_ID, Coach_Number),
                UNIQUE (Class)
            );
        """
        create_Ticket_table_sql = """
            CREATE TABLE Ticket (
                Ticket_ID NUMERIC(10),
                Cost DECIMAL(6,3),
                Train_ID NUMERIC(10),
                Class VARCHAR(15),
                Date DATE,
                Departure_Time TIME,
                Arrival_Time TIME,
                From_Station VARCHAR(30),
                To_Station VARCHAR(30),
                Passenger_ID NUMERIC(10),
                Coach_Number NUMERIC(4),
                Seat_no NUMERIC(3),
                PRIMARY KEY(Ticket_ID, Passenger_ID),
                FOREIGN KEY(Class) REFERENCES Coach(Class) ON DELETE NO ACTION
            );
        """
        create_Train_table_sql = """
            CREATE TABLE Train (
	            Name VARCHAR(20),
                Train_ID NUMERIC(10),
                FOREIGN KEY (Train_ID) REFERENCES Coach(Train_ID),
                PRIMARY KEY (Train_ID)
            );
        """
        create_Station_table_sql = """
            CREATE TABLE Station (
	            Name VARCHAR(30),
                Area VARCHAR(50),
                Governorate VARCHAR(40),
                PRIMARY KEY (Name)
            );
        """
        create_index_sql1 = "ALTER TABLE Coach ADD INDEX idx_class (Class);"
        create_index_sql2 = "ALTER TABLE Coach ADD INDEX idx_train_id (Train_ID);"

        # cursor = connection.cursor()
        # cursor.execute("drop Coach;")
        # cursor.execute("drop Station;")
        # cursor.execute("drop Ticket;")

        check_and_create_table(connection, 'Coach', create_Coach_table_sql)
        create_index_if_not_exists(connection, 'Coach', 'idx_class', create_index_sql1)
        check_and_create_table(connection, 'Ticket', create_Ticket_table_sql)
        #create_index_if_not_exists(connection, 'Coach', 'idx_train_id', create_index_sql2)
        check_and_create_table(connection, 'Train', create_Train_table_sql)
        check_and_create_table(connection, 'Station', create_Station_table_sql)
    else:
        print("Failed to establish a database connection")

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
        Construct_Database(connection)
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
            Construct_Database(connection)
            return connection
        except mysql.connector.Error as error:
            print("Failed to create Database:", error)
            return None

if __name__ == "__main__":
    ConnectToDatabase()