import sys
sys.dont_write_bytecode = True
import mysql.connector as sql
import CreateConnection

def print_receipt(ticket_id):
    try:
        # Connect to the database
        connection = CreateConnection.create()
        backEnd = connection.cursor()

        # Query the ticket table for the specified ticket_id
        query = """
        SELECT
            Ticket_ID,
            Together_ID,
            Cost,
            Class,
            Date,
            Departure_Time,
            Arrival_Time,
            From_Station,
            To_Station,
            Coach_Number,
            Seat_no,
            username
        FROM
            ticket
        WHERE
            Ticket_ID = %s
        """
        backEnd.execute(query, (ticket_id,))
        ticket = backEnd.fetchone()

        # Print the ticket details
        if ticket:
            print(f"Ticket ID: {ticket[0]}")
            print(f"Together ID: {ticket[1]}")
            print(f"Cost: {ticket[2]}")
            print(f"Class: {ticket[3]}")
            print(f"Date: {ticket[4]}")
            print(f"Departure Time: {ticket[5]}")
            print(f"Arrival Time: {ticket[6]}")
            print(f"From Station: {ticket[7]}")
            print(f"To Station: {ticket[8]}")
            print(f"Coach Number: {ticket[9]}")
            print(f"Seat Number: {ticket[10]}")
            print(f"Username: {ticket[11]}")
        else:
            print("Ticket not found.")

    except sql.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            backEnd.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    ticket_id = input("Enter Ticket ID: ")
    print_receipt(ticket_id)
