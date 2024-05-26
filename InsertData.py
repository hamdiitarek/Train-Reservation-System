import sys
sys.dont_write_bytecode = True
import CreateConnection

connection = CreateConnection.create()
backEnd = connection.cursor()

def create_train(Name, Train_ID):
    connection = CreateConnection.create()
    backEnd = connection.cursor()
    sql = "INSERT INTO Train (Name, Train_ID) VALUES (%s, %s)"
    val = (Name, Train_ID)
    backEnd.execute(sql, val)
    connection.commit()
    backEnd.close()
    connection.close()
    return True

def create_Coach(Train_ID, Coach_Number, Seats_array, Max_Seats):
    connection = CreateConnection.create()
    backEnd = connection.cursor()
    sql = "INSERT INTO Train (Train_ID, Coach_Number, Seats_array, Max_Seats) VALUES (%s, %s, %s, %s)"
    val = (Train_ID, Coach_Number, Seats_array, Max_Seats)
    backEnd.execute(sql, val)
    connection.commit()
    backEnd.close()
    connection.close()
    return True

def create_stations(stations):
    # Insert multiple stations into the database
    connection = CreateConnection.create()
    cursor = connection.cursor()
    sql = "INSERT INTO Station (Name, City) VALUES (%s, %s)"
    cursor.executemany(sql, stations)
    connection.commit()
    cursor.close()
    connection.close()
    return True  # Indicate successful batch insertion

def create_tickets(Ticket_ID, Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, username):
    connection = CreateConnection.create()
    backEnd = connection.cursor()
    sql = "INSERT INTO Ticket (Ticket_ID, Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, username) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)"
    val = (Ticket_ID, Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, username)

    backEnd.execute(sql, val)
    connection.commit()

    backEnd.close()
    connection.close()
    return True

def create_track(from_station, to_station, train_id):
    connection = CreateConnection.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Station WHERE Name IN (%s, %s)", (from_station, to_station))
    
    if cursor.fetchone()[0] != 2:
        raise ValueError("One or both stations do not exist: {}, {}".format(from_station, to_station))

    sql = "INSERT INTO Track (From_Station, To_Station, Train_ID) VALUES (%s, %s, %s)"
    val = (from_station, to_station, train_id)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    return True

stations = [ # I wont insert data cause safwat will change them lol # Doha changed them, kareem is good
    ("Scranton Business Park","Pensylvania"),
    ("Dunder Mifflin Inc.","New York"),
    ("Schrute Farms","California"),
    ("Electric City Sign","Washington"),
    ("New Hampshire","Nashua"),
    ("Connecticut","Stamford"),
    ("Utica","Utah"),
    ("Coopers","Texas"),
    ("Vance Refrigeration","Alabama"),
    ("Alfredo's Pizza Cafe","Minnesota"),
    ("Hooters","Los Angeles")
]
create_stations(stations)

create_train("Thomas", 21)
create_train("Percy", 32)
create_train("James", 10)
create_train("Edward", 17)
create_train("Gordon", 19)
create_train("Flynn", 49)
create_train("Henry", 33)
create_train("Diesel", 35)
create_train("Emily", 12)
create_train("Sheldon", 16)

train_assignments = {
    "main_track": 1,  # Train 1 for the main track
    "california_connect": 2,  # Train 2 for the California connection
    "washington_connect": 3,  # Train 3 for the Washington connection
    "nashua_connect": 4  # Train 4 for the Nashua connection
}


tracks_with_trains = {
    "main_track": [
        ("Vance Refrigeration", "Schrute Farms"),
        ("Schrute Farms", "Electric City Sign"),
        ("Electric City Sign", "New Hampshire"),
        ("New Hampshire", "Scranton Business Park")
    ],
    "california_connect": [
        ("Schrute Farms", "Hooters"),
        ("Hooters", "Alfredo's Pizza Cafe")
    ],
    "washington_connect": [
        ("Electric City Sign", "Utica"),
        ("Electric City Sign", "Coopers")
    ],
    "nashua_connect": [
        ("New Hampshire", "Connecticut"),
        ("New Hampshire", "Dunder Mifflin Inc.")
    ]
}

for key, train_id in train_assignments.items():
    for from_station, to_station in tracks_with_trains[key]:
        try:
            create_track(from_station, to_station, train_id)
        except ValueError as e:
            print(e)