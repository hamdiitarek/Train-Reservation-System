
# Please dont touch this file l7ad ma 2s7a we 2khosh el meeting
# 3andak mola7za ektebha bara

# i modified el sql schema

# el file dah el tneen by3ml kol 7aga (graph, booking, update stations list, test booking)


import sys
import mysql.connector
from collections import deque
from CreateConnection import connect
from datetime import datetime, timedelta

sys.dont_write_bytecode = True

def get_all_stations():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM Station")
    stations = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return stations

def get_routes():
    connection = connect()
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
        if to_station not in graph:
            graph[to_station] = []
        graph[from_station].append((to_station, train_id))
        graph[to_station].append((from_station, train_id)) #bidirectional routes

    queue = deque([[(start, None)]])
    visited = set()

    while queue:
        path = queue.popleft()
        station, current_train_id = path[-1]

        if station in visited:
            continue

        for next_station, next_train_id in graph.get(station, []):
            new_path = list(path)
            new_path.append((next_station, next_train_id))
            queue.append(new_path)
            if next_station == end:
                return new_path

        visited.add(station)
    
    return None


def book_ticket(ticket_id, departure_time, from_station, to_station, coach_number, seat_no, username):
    connection = connect()
    cursor = connection.cursor()
    try:
        routes = get_routes()
        route = find_route(routes, from_station, to_station)
        if not route:
            raise ValueError("No route found between {} and {}".format(from_station, to_station))
        
        last_departure_time = datetime.strptime(departure_time, "%H:%M")
        print(f"Starting at {from_station} at {last_departure_time.strftime('%H:%M')}")

        for i in range(len(route) - 1):
            station, current_track_id = route[i]
            next_station, next_track_id = route[i + 1]

            if i > 0 and current_track_id != next_track_id:
            # Assume 10 minutes to switch trains
                last_departure_time += timedelta(minutes=10)
                print(f"Switch trains at {station}. Next train (ID: {next_track_id}) departs at {last_departure_time.strftime('%H:%M')}")

            # Assume 1 hour travel time between stations (adjust as needed)
            travel_time = timedelta(hours=1)
            last_departure_time += travel_time
            print(f"Arrive at {next_station} at {last_departure_time.strftime('%H:%M')}")

        arrival_time = last_departure_time.strftime("%H:%M")
        
        # Use the train ID from the first segment of the journey
        first_train_id = route[1][1]
        
        sql = """
        INSERT INTO Ticket (Ticket_ID, Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, username)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (ticket_id, first_train_id, departure_time, arrival_time, from_station, to_station, coach_number, seat_no, username)
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
    for from_st, to_st in routes:
        if from_st == from_station or to_st == from_station:
            stations.add(to_st if from_st == from_station else from_st)
    return list(stations)

def update_from_station_list(to_station):
    routes = get_routes()
    stations = set()
    for from_st, to_st in routes:
        if from_st == to_station or to_st == to_station:
            stations.add(to_st if from_st == to_station else from_st)
    return list(stations)

#booking test
try:
    from_station = "Vance Refrigeration"
    to_station = "Connecticut"
    departure_time = "08:00"

    # Get the next available ticket ID from the database
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(Ticket_ID) FROM Ticket")
    last_ticket_id = cursor.fetchone()[0]
    ticket_id = last_ticket_id + 1 if last_ticket_id else 1

    book_ticket(ticket_id, departure_time, from_station, to_station, 1, 1, "omar")
except ValueError as e:
    print(e)



