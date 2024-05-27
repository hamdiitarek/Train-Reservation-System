
# Please dont touch this file l7ad ma 2s7a we 2khosh el meeting
# 3andak mola7za ektebha bara

# i modified el sql schema

# el file dah el tneen by3ml kol 7aga (graph, booking, update stations list, test booking)

import sys
sys.dont_write_bytecode = True

import mysql.connector
from collections import deque
from CreateConnection import create
from datetime import datetime, timedelta


def get_all_stations():
    connection = create()
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM Station")
    stations = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return stations

def get_routes():
    connection = create()
    cursor = connection.cursor()
    cursor.execute("SELECT From_Station, To_Station, Train_ID FROM Track")
    routes = cursor.fetchall()
    cursor.close()
    connection.close()
    return routes
    

def find_route(routes, start, end):
    
    graph = {}
    for from_station, to_station, train_id in routes:
        if from_station not in graph:
            graph[from_station] = []
        graph[from_station].append((to_station, train_id))

    queue = deque()
    queue.append(start)
    
    visited = set()
    visited.add(start)
    
    parentAndTrain = dict()
    parentAndTrain[start] = (start, None)
    
    while queue:
        station = queue.popleft()

        if station == end:
            break

        for next_station, next_train_id in graph[station]:
            if next_station not in visited:
                queue.append(next_station)
                visited.add(next_station)
                parentAndTrain[next_station] = [station, next_train_id]

    route = []
    station = end
    
    while (station in parentAndTrain) and station != parentAndTrain[station][0]:
        route.append([station, parentAndTrain[station][1]])
        station = parentAndTrain[station][0]
    
    if len(route) != 0:
        route.append([station, None])
        route.reverse()
        return route
    return None


def book_ticket(departure_time, from_station, to_station, username):
    
    connection = create()
    cursor = connection.cursor()
    
    # Get the next available ticket ID from the database
    cursor.execute("SELECT MAX(Together_ID) FROM Ticket")
    booked_together_id = cursor.fetchone()[0]
    booked_together_id = booked_together_id + 1 if booked_together_id else 1
    
    try:
        routes = get_routes()
        route = find_route(routes, from_station, to_station)
        
        if not route:
            raise ValueError("No route found between {} and {}".format(from_station, to_station))
        
        print(route)
        
        last_departure_time = datetime.strptime("{}:{}".format(departure_time, 0), "%H:%M")
        print(f"Starting at {from_station} at {last_departure_time.strftime('%H:%M')}")
        first_train_id = route[1][1]
        
        for i in range(len(route) - 1):
            [station, current_train_id] = route[i]
            [next_station, next_train_id] = route[i + 1]

            if i > 0 and current_train_id != next_train_id:
            # Assume 10 minutes to switch trains
                temp = last_departure_time;
                last_departure_time += timedelta(minutes=10)
                print(f"Switch trains at {station}. Next train (ID: {next_train_id}) departs at {last_departure_time.strftime('%H:%M')}")
                
                sql = """
                    SELECT sum(Seats_array)
                    FROM Coach
                    where Train_ID = {}
                """.format(first_train_id)
                
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
                """.format(seat, coach, first_train_id)

                cursor.execute(sql)
                
                sql = """
                INSERT INTO Ticket (Train_ID, Together_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, username)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                arrival_time = last_departure_time.strftime("%H:%M")
                val = (first_train_id, booked_together_id, departure_time, temp, from_station, station, coach, seat, username)
                cursor.execute(sql, val)
                connection.commit()
                departure_time = arrival_time
                first_train_id = next_train_id
                from_station = station

            # Assume 1 hour travel time between stations (adjust as needed)
            travel_time = timedelta(hours=1)
            last_departure_time += travel_time
            print(f"Arrive at {next_station} at {last_departure_time.strftime('%H:%M')}")

        arrival_time = last_departure_time.strftime("%H:%M")
        
        # Use the train ID from the first segment of the journey

        sql = """
            SELECT sum(Seats_array)
            FROM Coach
            where Train_ID = {}
        """.format(first_train_id)
                
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
        """.format(seat, coach, first_train_id)

        cursor.execute(sql)
        
        sql = """
        INSERT INTO Ticket (Train_ID, Together_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, username)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (first_train_id, booked_together_id, departure_time, arrival_time, from_station, to_station, coach, seat, username)
        cursor.execute(sql, val)
        connection.commit()
        
        print("Ticket booked successfully")
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        connection.rollback()
    finally:
        cursor.close()
        connection.close()



def update_to_station_list(from_station):
    
    routes = get_routes()
    stations = set()
    allStations = get_all_stations()
    
    for to_st in allStations:
        if to_st != from_station:
            route = find_route(routes, from_station, to_st)
            if route:
                stations.add(to_st)
    return list(stations)

def update_from_station_list(to_station):
    routes = get_routes()
    stations = set()
    for from_st, to_st in routes:
        if from_st == to_station or to_st == to_station:
            stations.add(to_st if from_st == to_station else from_st)
    return list(stations)

def get_time_routes(fStation):
    connection = create()
    cursor = connection.cursor()
    cursor.execute("SELECT To_Station, Train_ID, dept_time FROM Time_Track where From_Station = \"{}\"".format(fStation))
    routes = cursor.fetchall()
    cursor.close()
    connection.close()
    return routes

visited = set()

def findTimeRoute(fStation, tStation, target, Train_id, Dept_time):
    
    if tStation in visited:
        return []
    visited.add(tStation)
    
    if tStation == target:
        return [[fStation, tStation, Train_id, Dept_time]]
    
    arr = get_time_routes(tStation)
    
    for to_station, train_id, dept_time in arr:
        if dept_time - Dept_time == 2:
            ret = findTimeRoute(tStation, to_station, target, train_id, dept_time).copy()
            if len(ret) != 0:
                ret.append([fStation, tStation, Train_id, Dept_time])
                return ret      
    
    return []

def getCompleteRoute(fStation, tStation):
    l = []
    arr = get_time_routes(fStation)
    for to_station, train_id, dept_time in arr:
        visited.clear()
        ret = findTimeRoute(fStation, to_station, tStation, train_id, dept_time).copy()
        if len(ret) != 0:
            ret.reverse()
            l.append(ret)
    return l
        

def fetch_tickets(username):
        # Database connection to fetch tickets
        conn = create()
        cursor = conn.cursor()
        cursor.execute("SELECT Ticket_ID , Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, FROM Ticket WHERE username = %s group by Together_ID", (username,))
        tickets = cursor.fetchall()
        conn.close()
        return tickets

def delete_ticket(together_id):
    connecion = create()
    cursor = connecion.cursor()
    cursor.execute("DELETE FROM Ticket WHERE Together_ID = %s", (together_id,))
    connecion.commit()
    connecion.close()
    
#print(getCompleteRoute("New Hampshire", "Connecticut"))

#booking test
# try:
    # from_station = "Schrute Farms"
#     to_station = "Connecticut"
#     departure_time = "08:00"
#     book_ticket(departure_time, from_station, to_station, 1, 1, "omar")
    
#     from_station = "Schrute Farms"
#     to_station = "Connecticut"
#     departure_time = "08:00"
#     book_ticket(departure_time, from_station, to_station, 1, 3, "omar")
# except ValueError as e:
#     print(e)