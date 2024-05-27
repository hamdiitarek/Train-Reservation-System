import sys
sys.dont_write_bytecode = True

import tkinter.messagebox
import tkinter as tk
import customtkinter
import Booking
import GUI

# Assuming getCompleteRoute and its dependencies are defined elsewhere and imported here
# from your_module import getCompleteRoute

def booking_page(app):

    app.booking_frame = customtkinter.CTkFrame(app)
    app.booking_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    app.from_label = customtkinter.CTkLabel(app.booking_frame, text="From:")
    app.from_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

    app.from_entry = customtkinter.CTkOptionMenu(app.booking_frame, values=Booking.get_all_stations())
    app.from_entry.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="w")

    app.From_button = customtkinter.CTkButton(app.booking_frame, text="Update To Stations", command=lambda: update_to_stations(app))
    app.From_button.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="e")

    app.to_label = customtkinter.CTkLabel(app.booking_frame, text="To:")
    app.to_label.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")

    app.to_entry = customtkinter.CTkOptionMenu(app.booking_frame, values=[])
    app.to_entry.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="w")

    app.to_button = customtkinter.CTkButton(app.booking_frame, text="Update List of trains", command=lambda: update_available_trains(app, None))
    app.to_button.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="e")
    
    app.book_button = customtkinter.CTkButton(app.booking_frame, text="Book", command=lambda: book_tickets(app))
    app.book_button.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 10), sticky="ew")

    app.available_trains_label = customtkinter.CTkLabel(app.booking_frame, text="Available Trains:")
    app.available_trains_label.grid(row=3, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")

    app.available_trains_listbox = tk.Listbox(app.booking_frame)
    app.available_trains_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=(5, 10), sticky="nsew")

    app.booking_frame.grid_columnconfigure(0, weight=1)
    app.booking_frame.grid_columnconfigure(1, weight=1)
    app.booking_frame.grid_columnconfigure(2, weight=1)
    app.booking_frame.grid_rowconfigure(4, weight=1)

def printTickets(app):
    # username = app.
    return 0

def modify_ticket(app):
    Username = GUI.App.UserName 
    tickets = Booking.fetch_tickets(Username)

    app.available_trains_listbox = tk.Listbox(app.booking_frame)
    app.available_trains_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=(5, 10), sticky="nsew")
    app.available_trains_listbox.delete(0, tk.END)
    for ticket in tickets:
        ticket_str = f"Ticket ID: {ticket[0]} Train ID: {ticket[1]} Departure Time: {ticket[2]} Arrival Time: {ticket[3]} From Station: {ticket[4]} To Station: {ticket[5]} Coach Number: {ticket[6]} Seat Number: {ticket[7]}"
        app.available_trains_listbox.insert(tk.END, ticket_str)
    app.booking_frame.grid_columnconfigure(0, weight=1)
    app.booking_frame.grid_columnconfigure(1, weight=1)
    app.booking_frame.grid_columnconfigure(2, weight=1)
    app.booking_frame.grid_rowconfigure(4, weight=1)

    


def update_to_stations(app):
    from_station = app.from_entry.get()
    to_stations = Booking.update_to_station_list(from_station)
    app.to_entry.configure(values=to_stations)
    app.to_entry.set("")
    

def update_available_trains(app, event):
    from_location = app.from_entry.get()
    to_location = app.to_entry.get()

    if not from_location or not to_location:
        tkinter.messagebox.showwarning("Selection Missing", "Please select both From and To stations.")
        return

    routes = Booking.getCompleteRoute(from_location, to_location)

    app.available_trains_listbox.delete(0, tk.END)
    for route in routes:
        route_str = " -> ".join([f"{fStation} (Train {Train_id} at {Dept_time})" for fStation, tStation, Train_id, Dept_time in route])
        app.available_trains_listbox.insert(tk.END, route_str)

def book_tickets(app):
    
    selected_trains = app.available_trains_listbox.curselection()
    
    if not selected_trains:
        tkinter.messagebox.showwarning("No Selection", "Please select a train to book.")
        return

    from_location = app.from_entry.get()
    to_location = app.to_entry.get()
    routes = Booking.getCompleteRoute(from_location, to_location)
    choice = list(selected_trains)
    route = routes[choice[0]]
    Booking.book_ticket(route[0][3], route[0][0], route[-1][0], app.getUsername())
 
    selected_trains_list = [app.available_trains_listbox.get(i) for i in selected_trains]
    tkinter.messagebox.showinfo("Booking Successful", f"Tickets booked for: {', '.join(selected_trains_list)}")
    clear_booking_form(app)

def clear_booking_form(app):
    app.from_entry.set("")
    app.to_entry.set("")
    app.available_trains_listbox.delete(0, tk.END)

def other_features(app):
    tkinter.messagebox.showinfo("Feature", "This is a placeholder for features.")

# Assume the app initialization and mainloop are elsewhere in your application