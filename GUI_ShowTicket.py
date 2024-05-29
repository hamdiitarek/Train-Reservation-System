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

    app.view_button = customtkinter.CTkButton(app.showticket_frame, text="View Ticket Info", command=lambda: details_ticket(app))
    app.view_button.grid(row=9, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

    app.delete_button = customtkinter.CTkButton(app.showticket_frame, text="Delete Ticket", command=lambda: delete_ticket(app))
    app.delete_button.grid(row=9, column=2, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

    app.textbox = customtkinter.CTkTextbox(app.showticket_frame, width=400, corner_radius=0)
    app.textbox.grid(row=10, column=0, columnspan=4, padx=10, pady=(5, 10), sticky="nsew")
    # app.textbox.insert("0.0", "Some example text!\n" * 50)

    app.showticket_frame.grid_columnconfigure(0, weight=1)
    app.showticket_frame.grid_columnconfigure(1, weight=1)
    app.showticket_frame.grid_columnconfigure(2, weight=1)
    app.showticket_frame.grid_columnconfigure(3, weight=1)
    app.showticket_frame.grid_rowconfigure(12, weight=1)


def update_tickets(app, event):
    
    username = app.getUsername()
    bookings = Booking.fetch_tickets(username)
    
    bookingsArray = [] 
    for together_id in bookings.keys():
        bookingsArray.append(bookings[together_id])
    app.setBookings(bookingsArray)
    
    app.my_tickets_listbox.delete(0, tk.END)
    for together_id in bookings.keys():
        
        together_str = "Ticket #: {}".format(together_id)
        together_str = together_str.ljust(20)
        
        dept_str = "{} - ".format(bookings[together_id][0][2])
        arrive_str = "{}".format(bookings[together_id][-1][3])
        
        time = dept_str + arrive_str
        time = time.ljust(40)
        
        from_str = "From: {}".format(bookings[together_id][0][4])
        from_str = from_str.ljust(40)
        
        to_str = "To: {}".format(bookings[together_id][-1][5])
        to_str = to_str.ljust(40)
        
        price = 0
        
        for i in bookings[together_id]:
            price = price + i[8]
            
        price_str = "Price: ${}.00".format(int(price))
        
        ticket_str = together_str + time + from_str + to_str + price_str
        app.my_tickets_listbox.insert(tk.END, ticket_str)

def details_ticket(app):
    
    selected_ticket = app.my_tickets_listbox.curselection()
    
    if not selected_ticket:
        tkinter.messagebox.showwarning("No Selection", "Please select ticket")
        return
    
    choice = list(selected_ticket)[0]
    booking = app.getBookings()
    booking = booking[choice]
    
    app.textbox.delete("0.0", "end")
    str_info = "Please read the following carefully:\n"
    
    for ticket in booking:
        str_info = str_info + "You will board   train #{} coach #{}   at {},    {} station.   Your seat number is {}\n".format(
            ticket[1], ticket[6], ticket[2], ticket[4], ticket[7]
        )
        
    str_info = str_info + "\n\nTrain stops at the following stations:\n"
    
    from_station = booking[0][4]
    to_station = booking[-1][5]
    Dept_time = booking[0][2].total_seconds() / (60 * 60)
    Arr_time = (booking[-1][3].total_seconds() + 5 * 60) / (60 * 60)
    
    route = Booking.getCompleteRoute(from_station, to_station)
    
    for i in route:
        if i[0][3] == Dept_time and i[-1][3] + 2 == Arr_time:
            route = i
            break
        
    for i in route:
        str_info = str_info + "{} station   at {}:55\n".format(i[1], i[3] + 1)
        
    app.textbox.insert("0.0", str_info)
    

def delete_ticket(app):
    
    selected_ticket = app.my_tickets_listbox.curselection()
    
    if not selected_ticket:
        tkinter.messagebox.showwarning("No Selection", "Please select first to delete ticket.")
        return
 
    selected_trains_list = [app.my_tickets_listbox.get(i) for i in selected_ticket]
    str_selected = selected_trains_list[0]
    str_selected = str_selected.split(' ')
    together_id = str_selected[2]
    together_id = int(together_id)
    
    Booking.delete_ticket(together_id, app.getUsername())
    tkinter.messagebox.showinfo("Deletion Successful", f"Tickets deleted for: {', '.join(selected_trains_list)}")
    
    update_tickets(app, None)
    app.textbox.delete("0.0", "end")
   # clear_booking_form(app)