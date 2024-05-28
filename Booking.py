import sys
sys.dont_write_bytecode = True

import mysql.connector
from collections import deque
from CreateConnection import create


def get_all_stations():
    connection = create()
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM Station")
    stations = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return stations

def getSeats(Train_ID):
    
    connection = create()
    cursor = connection.cursor()
    
    sql = """
        SELECT sum(Seats_array)
        FROM Coach
        where Train_ID = {}
    """.format(Train_ID)
      
    cursor.execute(sql)
    seat = cursor.fetchone()
    seat = list(seat)
    seat = seat[0]
    
    if (seat >= 100):
        print("train is full")
        return
        
    coach = (seat // 25) + 1
    seat = (seat % 25) + 1

    sql = """
        update coach
        set Seats_array = {}
        where Coach_Number = {} and Train_ID = {};
    """.format(seat, coach, Train_ID)

    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    return seat, coach

def neighbours(fStation):
    connection = create()
    cursor = connection.cursor()
    cursor.execute("SELECT To_Station, Train_ID, dept_time FROM Time_Track where From_Station = \"{}\"".format(fStation))
    routes = cursor.fetchall()
    cursor.close()
    connection.close()
    return routes

visited = set()

def dfs_findTimeRoute(fStation, tStation, target, Train_id, Dept_time):
    
    if tStation in visited:
        return []
    visited.add(tStation)
    
    if tStation == target:
        return [[fStation, tStation, Train_id, Dept_time]]
    
    arr = neighbours(tStation)
    for to_station, train_id, dept_time in arr:
        if dept_time - Dept_time == 2:
            ret = dfs_findTimeRoute(tStation, to_station, target, train_id, dept_time).copy()
            if len(ret) != 0:
                ret.append([fStation, tStation, Train_id, Dept_time])
                return ret      
    
    return []

def getCompleteRoute(fStation, tStation):
    l = []
    
    arr = neighbours(fStation)
    for to_station, train_id, dept_time in arr:
        visited.clear()
        ret = dfs_findTimeRoute(fStation, to_station, tStation, train_id, dept_time).copy()
        if len(ret) != 0:
            ret.reverse()
            l.append(ret)
            
    visited.clear()
    return l

def dfs_find_reachable(fStation, Dept_time, total_time, target):
    
    if (fStation) in visited:
        return
    visited.add(fStation)
    
    if total_time == 24:
        return
    
    arr = neighbours(fStation)
    for to_station, train_id, dept_time in arr:
        if to_station != target and dept_time - Dept_time == 2:
            dfs_find_reachable(to_station, dept_time, total_time + 2, target)

def find_to_station_list(fStation):
    
    l = []
    
    arr = neighbours(fStation)
    for to_station, train_id, dept_time in arr:
        visited.clear()
        dfs_find_reachable(to_station, dept_time, 2, fStation)
        l.append(visited.copy())
    
    to_stations = set()
    
    for i in l:
        for j in i:
            to_stations.add(j)
            
    to_stations = list(to_stations)
    to_stations.sort()
    
    visited.clear()
    return to_stations
        
def book_ticket(route, username):
    
    connection = create()
    cursor = connection.cursor()
    
    # Get the next available ticket ID from the database
    cursor.execute("SELECT MAX(Together_ID) FROM Ticket")
    booked_together_id = cursor.fetchone()[0]
    booked_together_id = booked_together_id + 1 if booked_together_id else 1
        
    tickets = []
    last = 0
    
    for i in range(1, len(route)):
        if route[i][2] != route[i - 1][2]:
            tickets.append([last, i - 1])
            last = i
            
    if tickets[-1] != [last, len(route) - 1]:
        tickets.append([last, len(route) - 1])

    for trips in tickets:
        
        train_id = route[trips[0]][2]
        departure_time = "{}:0".format(route[trips[0]][3])
        arrival_time = "{}:55".format(route[trips[1]][3] + 1)
        from_station = route[trips[0]][0]
        to_station = route[trips[1]][1]
        seat, coach = getSeats(route[trips[0]][2])
        
        sql = """
            INSERT INTO Ticket (Train_ID, Together_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, username)
            VALUES ({}, {}, \"{}\", \"{}\", \"{}\", \"{}\", {}, {}, \"{}\")
        """.format(train_id, booked_together_id, departure_time, arrival_time, from_station, to_station, coach, seat, username)
        
        cursor.execute(sql)
        connection.commit()

    cursor.close()
    connection.close()

def fetch_tickets(username):
    
    conn = create()
    cursor = conn.cursor()
    
    sql = """
        select distinct(Together_ID)
        from Ticket
        where username = \"{}\"
    """.format(username)
    
    cursor.execute(sql)
    together_IDS = cursor.fetchall()
    tickets_Together = dict()
    
    # together_id -> list()
    
    for together_id in together_IDS:
    
        together_id = list(together_id)
        together_id = together_id[0]
        
        sql = """
            select Ticket_ID, Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, ((time_to_sec(Arrival_Time) - time_to_sec(Departure_Time) + 5*60)/60/60) as price
            from Ticket
            where username = \"{}\" and Together_ID = {}
            order by Ticket_ID;
        """.format(username, together_id)
        
        cursor.execute(sql)
        arr = cursor.fetchall()
        tickets_Together[together_id] = list()
        
        for j in arr:
            tickets_Together[together_id].append(j)
    
    cursor.close()
    conn.close()
    return tickets_Together

def delete_ticket(together_id, username):
    connecion = create()
    cursor = connecion.cursor()
    cursor.execute("DELETE FROM Ticket WHERE Together_ID = {} and username = \"{}\"".format(together_id, username))
    connecion.commit()
    cursor.close()
    connecion.close()

# print()
print(fetch_tickets("omar"))
#print(getCompleteRoute("New Hampshire", "Connecticut"))