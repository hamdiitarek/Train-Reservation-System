import sys

sys.dont_write_bytecode = True
import mysql.connector as sql
import CreateConnection


def create_train(Name, Train_ID):
    connection = CreateConnection.create()
    backEnd = connection.cursor()
    sql = "INSERT IGNORE INTO Train (Name, Train_ID) VALUES (%s, %s)"
    val = (Name, Train_ID)
    backEnd.execute(sql, val)
    connection.commit()
    backEnd.close()
    connection.close()
    return True


def create_Coach(Train_ID, Coach_Number, Seats_taken):
    connection = CreateConnection.create()
    backEnd = connection.cursor()
    sql = "INSERT IGNORE INTO Train (Train_ID, Coach_Number, Seats_taken) VALUES (%s, %s, %s)"
    val = (Train_ID, Coach_Number, Seats_taken)
    backEnd.execute(sql, val)
    connection.commit()
    backEnd.close()
    connection.close()
    return True


def create_stations(stations):
    # Insert multiple stations into the database
    connection = CreateConnection.create()
    cursor = connection.cursor()

    sql = "INSERT IGNORE INTO Station (Name, City) VALUES (%s, %s)"
    cursor.executemany(sql, stations)
    connection.commit()
    cursor.close()
    connection.close()
    return True  # Indicate successful batch insertion


def create_tickets(
    Ticket_ID,
    Train_ID,
    Departure_Time,
    Arrival_Time,
    From_Station,
    To_Station,
    Coach_Number,
    Seat_no,
    username,
):
    connection = CreateConnection.create()
    backEnd = connection.cursor()
    sql = "INSERT IGNORE INTO Ticket (Ticket_ID, Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, username) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)"
    val = (
        Ticket_ID,
        Train_ID,
        Departure_Time,
        Arrival_Time,
        From_Station,
        To_Station,
        Coach_Number,
        Seat_no,
        username,
    )

    backEnd.execute(sql, val)
    connection.commit()

    backEnd.close()
    connection.close()
    return True


def create_track(from_station, to_station, train_id):
    connection = CreateConnection.create()
    cursor = connection.cursor()
    
    # sql = """select From_Station, To_Station, Train_ID from track
    #          where From_Station = %s and To_Station = %s and Train_ID = %s"""
    # val = (from_station, to_station, train_id)
    # cursor.execute(sql, val)
    
    # if (cursor.fetchone()):
    sql = "INSERT IGNORE INTO Track (From_Station, To_Station, Train_ID) VALUES (%s, %s, %s)"
    val = (from_station, to_station, train_id)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    return True
    # else:
    #     return False

def create_time_track(from_station, to_station, train_id, time):
    connection = CreateConnection.create()
    cursor = connection.cursor()

    # sql = """select From_Station, To_Station, Train_ID from track
    #          where From_Station = %s and To_Station = %s and Train_ID = %s"""
    # val = (from_station, to_station, train_id)
    # cursor.execute(sql, val)

    # if (cursor.fetchone()):
    sql = "INSERT IGNORE INTO Time_Track (From_Station, To_Station, Train_ID, dept_time) VALUES (%s, %s, %s, %s)"
    val = (from_station, to_station, train_id, time)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    return True
    # else:
    #     return False

def insert_coaches_in_trains():
    try:
        # Connect to the database
        connection = CreateConnection.create()
        backEnd = connection.cursor()

        # Select all trains
        backEnd.execute("SELECT Train_ID FROM Train")
        trains = backEnd.fetchall()

        # Insert four coaches for each train
        for train in trains:
            train_id = train[0]
            for coach_number in range(1, 5):
                backEnd.execute(
                    "INSERT IGNORE INTO coach (Train_ID, Coach_Number, Seats_taken) VALUES (%s, %s, %s)",
                    (train_id, coach_number, 0),
                )

        # Commit the transaction
        connection.commit()

    except sql.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            backEnd.close()
            connection.close()


stations = [  # I wont insert data cause safwat will change them lol # Doha changed them, kareem is good
    # ("Scranton Business Park","Pensylvania"),
    ("Dunder Mifflin Inc.", "New York"),
    ("Schrute Farms", "California"),
    ("Electric City Sign", "Washington"),
    ("New Hampshire", "Nashua"),
    ("Connecticut", "Stamford"),
    ("Utica", "Utah"),
    ("Coopers", "Texas"),
    # ("Vance Refrigeration","Alabama"),
    ("Alfredo's Pizza Cafe", "Minnesota"),
    ("Hooters", "Los Angeles"),
    ("Cozy Corner Diner", "California"),  # first point main track
    ("The Codfather", "Washington"),
    ("The Sandy Chestnut", "Washington"),
    ("Lawn Order", "Nashua"),  # last point main track
    (
        "Sofa So Good",
        "California",
    ),  # first california-corner left (starts in schrute, california)
    ("Blue Sky Boutique", "California"),
    ("Crystal Waters Spa", "California"),
    ("Velvet Petals Florist", "Minnesota"),
    (
        "Timeless Elegance",
        "Minnesota",
    ),  # last california-corner left (ends in alfredo, minnesota)
    (
        "El Ateneo Grand Splendid",
        "California",
    ),  # first california-corner right (starts in schrute, california)
    ("Bamford Haybarn", "California"),
    ("Petaling Street Market", "California"),
    ("Queen Victoria Market", "Los Angelos"),
    (
        "FairPrice Finest",
        "Los Angelos",
    ),  # last california-corner right (ends in hooters, los angelos)
    (
        "Camden Market",
        "Washington",
    ),  # first washington-corner left  (starts in electric, washington)
    (
        "BooksActually",
        "Texas",
    ),  # last washington-corner left (starts in coopers, texas)
    (
        "Mercado de San Miguel",
        "Washington",
    ),  # first washington-corner right  (starts in electric, washington)
    (
        "Lotte Department Store",
        "Utah",
    ),  # last washington-corner right (starts in uticah, utah)
    (
        "Tienda DUMBO",
        "Nashua",
    ),  # first Nashua-corner left (starts in new hampshire, nashua)
    ("Golden Horizon", "Nashua"),
    ("Morning Mist", "Nashua"),
    ("Serendipity Finds", "New York"),
    ("Evergreen Adventures", "New York"),
    ("Tranquil Path Yoga", "Nashua"),  # First point
    ("Rizzoli Bookstore", "Nashua"),
    ("LuxoPlaza", "Nashua"),
    ("AuraPlaza", "Stamford"),
    ("St George's Market", "Stamford"),  # last point
]

train_assignments = {
    "main_track": [21, 10, 12],  # Train 1 for the main track
    "california_connect_left": [
        32,
        17,
        12,
    ],  # Train 2 for the California left connection
    "california_connect_right": [
        11,
        29,
        12,
    ],  # Train 2 for the California right connection
    "washington_connect_left": [
        19,
        49,
        6,
    ],  # Train 3 for the Washington left connection
    "washington_connect_right": [
        12,
        16,
        6,
    ],  # Train 3 for the Washington right connection
    "nashua_connect_left": [33, 35, 12],  # Train 4 for the Nashua left connection
    "nashua_connect_right": [77, 45, 12],  # Train 4 for the Nashua right connection
}

tracks_with_trains = {
    "main_track": [
        ("Schrute Farms", "Cozy Corner Diner"),  # main station - 1st point
        ("Cozy Corner Diner", "The Codfather"),  # 1st point - 2nd point
        ("The Codfather", "Electric City Sign"),  # 2nd point - main station
        ("Electric City Sign", "The Sandy Chestnut"),
        ("The Sandy Chestnut", "Lawn Order"),
        ("Lawn Order", "New Hampshire"),
    ],
    "california_connect_left": [
        ("Schrute Farms", "Sofa So Good"),
        ("Sofa So Good", "Blue Sky Boutique"),
        ("Blue Sky Boutique", "Crystal Waters Spa"),
        ("Crystal Waters Spa", "Velvet Petals Florist"),
        ("Velvet Petals Florist", "Timeless Elegance"),
        ("Timeless Elegance", "Alfredo's Pizza Cafe"),
    ],
    "california_connect_right": [
        ("Schrute Farms", "El Ateneo Grand Splendid"),
        ("El Ateneo Grand Splendid", "Bamford Haybarn"),
        ("Bamford Haybarn", "Petaling Street Market"),
        ("Petaling Street Market", "Queen Victoria Market"),
        ("Queen Victoria Market", "FairPrice Finest"),
        ("FairPrice Finest", "Hooters"),
    ],
    "washington_connect_left": [
        ("Electric City Sign", "Camden Market"),
        ("Camden Market", "BooksActually"),
        ("BooksActually", "Coopers"),
    ],
    "washington_connect_right": [
        ("Electric City Sign", "Mercado de San Miguel"),
        ("Mercado de San Miguel", "Lotte Department Store"),
        ("Lotte Department Store", "Utica"),
    ],
    "nashua_connect_left": [
        ("New Hampshire", "Tienda DUMBO"),
        ("Tienda DUMBO", "Golden Horizon"),
        ("Golden Horizon", "Morning Mist"),
        ("Morning Mist", "Serendipity Finds"),
        ("Serendipity Finds", "Evergreen Adventures"),
        ("Evergreen Adventures", "Dunder Mifflin Inc."),
    ],
    "nashua_connect_right": [
        ("New Hampshire", "Tranquil Path Yoga"),
        ("Tranquil Path Yoga", "Rizzoli Bookstore"),
        ("Rizzoli Bookstore", "LuxoPlaza"),
        ("LuxoPlaza", "AuraPlaza"),
        ("AuraPlaza", "St George's Market"),
        ("St George's Market", "Connecticut"),
    ],
}


def byHand():
    #print(len(stations))
    create_stations(stations)

    create_train("Thomas", 21)  # main track
    create_train("Thomas", 210)  # main track
    create_train("James", 10)  # main track
    create_train("James", 100)  # main track
    create_train("Percy", 32)  # california
    create_train("Percy", 320)  # california
    create_train("Edward", 17)  # california
    create_train("Edward", 170)  # california
    create_train("Gordon", 19)  # washington
    create_train("Gordon", 190)  # washington
    create_train("Flynn", 49)  # washington
    create_train("Flynn", 490)  # washington
    create_train("Henry", 33)  # nashua
    create_train("Henry", 330)  # nashua
    create_train("Diesel", 35)  # nashua
    create_train("Diesel", 350)  # nashua
    create_train("Emily", 12)  # california-LA
    create_train("Emily", 120)  # california-LA
    create_train("Sheldon", 16)  # california-LA
    create_train("Sheldon", 160)  # california-LA
    create_train("Colby", 45)  # Washington-Utah
    create_train("Colby", 450)  # Washington-Utah
    create_train("Leanord", 77)  # Washington-Utah
    create_train("Leanord", 770)  # Washington-Utah
    create_train("Penny", 29)  # Nashua- straford
    create_train("Penny", 290)  # Nashua- straford
    create_train("koothropali", 11)  # Nashua- straford
    create_train("koothropali", 110)  # Nashua- straford

    insert_coaches_in_trains()
    
    # for key, train_id in train_assignments.items():
    #     for from_station, to_station in tracks_with_trains[key]:
    #         try:
    #             create_track(from_station, to_station, train_id[0])
    #             create_track(to_station, from_station, train_id[1])
    #         except ValueError as e:
    #             print(e)

    for key, train_id in train_assignments.items():

        counter = 0

        for from_station, to_station in tracks_with_trains[key]:
            create_time_track(from_station, to_station, train_id[0], counter)
            create_time_track(from_station, to_station, train_id[1], counter + train_id[2])
            counter = counter + 2

        l = tracks_with_trains[key].copy()
        l.reverse()
        counter = 0

        for to_station, from_station in l:
            create_time_track(from_station, to_station, train_id[1] * 10, counter)
            create_time_track(from_station, to_station, train_id[0] * 10, counter + train_id[2])
            counter = counter + 2
