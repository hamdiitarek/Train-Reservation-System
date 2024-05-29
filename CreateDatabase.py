import sys
sys.dont_write_bytecode = True

from mysql.connector import Error

import CreateConnection

def check_and_create_table(backEnd, table_name, create_table_sql):
    backEnd.execute("CREATE TABLE IF NOT EXISTS {}".format(table_name + create_table_sql))

def create_view(backEnd, view_name, view_sql):
    try:
        backEnd.execute(f"DROP VIEW IF EXISTS {view_name}")
        backEnd.execute("CREATE VIEW {0} as {1}".format(view_name, view_sql))
        print("View created successfully")
    except Error as e:
        print(f"Error: '{e}'")

def Construct_Database():
    
    create_users_table_sql = """
    (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        salt VARCHAR(255) NOT NULL
    );
    """
    
    create_Train_table_sql = """
    (
        Name VARCHAR(20),
        Train_ID NUMERIC(10),
        PRIMARY KEY (Train_ID)
    );
    """
    
    create_Station_table_sql = """
    (
        Name VARCHAR(60),
        City VARCHAR(20),
        PRIMARY KEY (Name)
    );
    """

    create_Coach_table_sql = """
    (
        Train_ID NUMERIC(10),
        Coach_Number NUMERIC(1),
        Seats_taken NUMERIC(8),
        PRIMARY KEY(Train_ID, Coach_Number),
        FOREIGN KEY(Train_ID) references Train(Train_ID)
    );
    """
    
    create_Ticket_table_sql = """
    (
        Ticket_ID int auto_increment,
        Together_ID int,
        Train_ID NUMERIC(10),
        Departure_Time TIME,
        Arrival_Time TIME,
        From_Station VARCHAR(60),
        To_Station VARCHAR(60),
        Coach_Number NUMERIC(1),
        Seat_no NUMERIC(3),
        username VARCHAR(50),
        PRIMARY KEY(Ticket_ID),
        FOREIGN KEY(Train_ID, Coach_Number) references Coach(Train_ID, Coach_Number),
		FOREIGN KEY(username) REFERENCES users(username) ON DELETE NO ACTION,
        FOREIGN KEY(To_Station) references Station(Name),
        FOREIGN KEY(From_Station) references Station(Name)
    );
    """
    
    create_Time_Track_table_sql = """
    (
        From_Station VARCHAR(60),
        To_Station VARCHAR(60),
        Train_ID NUMERIC(10),
        dept_time NUMERIC(2),
        FOREIGN KEY(To_Station) references Station(Name),
        FOREIGN KEY(From_Station) references Station(Name),
        FOREIGN KEY(Train_ID) references Train(Train_ID),
        PRIMARY KEY(To_Station, From_Station, dept_time)
    );          
    """

    Tickets_View = """
        SELECT username,Together_ID, Ticket_ID, Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, ((time_to_sec(Arrival_Time) - time_to_sec(Departure_Time) + 5*60)/60/60)/2 * 25 as price
        FROM Ticket;
    """
    
    Revenue_View = """
        SELECT TR.Train_ID as Train_ID , TR.Name as Train_Name, SUM(((time_to_sec(TC.Arrival_Time) - time_to_sec(TC.Departure_Time) + 5*60)/60/60)/2 * 25) as Total_Train_Revenue
        FROM TICKET as TC, TRAIN as TR
        WHERE TC.Train_ID = TR.Train_ID
        group by TR.Train_ID;
    """

    connection = CreateConnection.create()
    backEnd = connection.cursor()
    
    check_and_create_table(backEnd, 'users', create_users_table_sql)
    check_and_create_table(backEnd, 'Train', create_Train_table_sql)
    check_and_create_table(backEnd, 'Station', create_Station_table_sql)
    check_and_create_table(backEnd, 'Coach', create_Coach_table_sql)
    check_and_create_table(backEnd, 'Ticket', create_Ticket_table_sql)
    check_and_create_table(backEnd, 'Time_Track', create_Time_Track_table_sql)

    create_view(backEnd, 'SHOW_TICKETS', Tickets_View)
    create_view(backEnd, 'REVENUE', Revenue_View)
    
    backEnd.close()
    connection.close()