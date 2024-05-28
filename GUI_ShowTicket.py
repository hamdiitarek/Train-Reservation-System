import sys
sys.dont_write_bytecode = True

import tkinter.messagebox
import tkinter as tk
import customtkinter
import GUI
import Booking

def ShowTicket(app):
    
    app.showticket_frame = customtkinter.CTkFrame(app)
    app.showticket_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    app.all_tickets_label = customtkinter.CTkLabel(app.showticket_frame, text="Tickets")
    app.all_tickets_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(5, 10), sticky="nsew")

    app.all_tickets_button = customtkinter.CTkButton(app.showticket_frame, text="Refresh Tickets", command=lambda: update_tickets(app, None))
    app.all_tickets_button.grid(row=1, column=0, columnspan=4, padx=10, pady=(5, 10), sticky="nsew")

    app.my_tickets_label = customtkinter.CTkLabel(app.showticket_frame, text="Your Booked Tickets:")
    app.my_tickets_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="w")

    app.my_tickets_listbox = tk.Listbox(app.showticket_frame, font=("Arial", 16))
    app.my_tickets_listbox.grid(row=3, column=0,rowspan=6, columnspan=4, padx=10, pady=(5, 10), sticky="nsew")

    app.view_button = customtkinter.CTkButton(app.showticket_frame, text="View Ticket Info", command=None)
    app.view_button.grid(row=9, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

    app.delete_button = customtkinter.CTkButton(app.showticket_frame, text="Delete Ticket", command=None)
    app.delete_button.grid(row=9, column=2, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")


    app.textbox = customtkinter.CTkTextbox(app.showticket_frame, width=400, corner_radius=0)
    app.textbox.grid(row=10, column=0, columnspan=4, padx=10, pady=(5, 10), sticky="nsew")
    app.textbox.insert("0.0", "Some example text!\n" * 50)

    app.showticket_frame.grid_columnconfigure(0, weight=1)
    app.showticket_frame.grid_columnconfigure(1, weight=1)
    app.showticket_frame.grid_columnconfigure(2, weight=1)
    app.showticket_frame.grid_columnconfigure(3, weight=1)
    app.showticket_frame.grid_rowconfigure(12, weight=1)

def update_tickets(app, event):
    username = app.getUsername()

    fetch = Booking.fetch_tickets(username)

    app.my_tickets_listbox.delete(0, tk.END)
    for together_id, tickets in fetch.items():
        for ticket in tickets:
            Ticket_ID, Train_ID, Departure_Time, Arrival_Time, From_Station, To_Station, Coach_Number, Seat_no, price = ticket
            ticketStr = f"Ticket {Ticket_ID}: {From_Station} to {To_Station} on {Train_ID} at {Departure_Time} - {Arrival_Time}, Coach {Coach_Number}, Seat {Seat_no}, Price: ${price:.2f}"
            app.my_tickets_listbox.insert(tk.END, ticketStr)

def delete_ticket(app):
    
    selected_ticket = app._listbox.curselection()
    
    if not selected_ticket:
        tkinter.messagebox.showwarning("No Selection", "Please select first to delete ticket.")
        return

    routes = app.getRoutes()
    choice = list(selected_ticket)
    route = routes[choice[0]]
 
    selected_trains_list = [app.my_tickets_listbox.get(i) for i in selected_ticket]
    tkinter.messagebox.showinfo("Deletion Successful", f"Tickets deleted for: {', '.join(selected_trains_list)}")
   # clear_booking_form(app)


