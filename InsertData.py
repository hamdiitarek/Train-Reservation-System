import sys
sys.dont_write_bytecode = True

import CreateConnection

connection = CreateConnection.create()
backEnd = connection.cursor()

def create_train(Name, Train_ID):
    sql = "INSERT INTO Train (Name, Train_ID) VALUES (%s, %s)"
    val = (Name, Train_ID)

    backEnd.execute(sql, val)
    connection.commit()

    backEnd.close()
    connection.close()
    return True

def create_Coach(Train_ID, Coach_Number, Seats_array, Max_Seats):
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
    
    sql = "INSERT INTO Station (Name, Area, Governorate) VALUES (%s, %s, %s)"
    
    cursor.executemany(sql, stations)
    connection.commit()
    
    cursor.close()
    connection.close()
    return True  # Indicate successful batch insertion

stations = [ # I wont insert data cause safwat will change them lol
    ()
    ()
    ()
    ()
    ()
    ()
    ()
    ()
    ()
    ()
    ()
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