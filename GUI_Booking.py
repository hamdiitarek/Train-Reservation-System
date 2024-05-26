import sys
sys.dont_write_bytecode = True
import tkinter.messagebox
import tkinter as tk
import customtkinter
from GUI_ui import clear_main_content

def booking_page(app):
    clear_main_content(app)

    app.booking_frame = customtkinter.CTkFrame(app)
    app.booking_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    app.from_label = customtkinter.CTkLabel(app.booking_frame, text="From:")
    app.from_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

    app.from_entry = customtkinter.CTkOptionMenu(app.booking_frame, values=[
        "Scranton Business Park",
        "Dunder Mifflin Inc.",
        "Schrute Farms",
        "Electric City Sign",
        "New Hampshire",
        "Connecticut",
        "Utica",
        "Coopers",
        "Vance Refrigeration",
        "Alfredo's Pizza Cafe",
        "Hooters"
        ])
    app.from_entry.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="w")

    app.to_label = customtkinter.CTkLabel(app.booking_frame, text="To:")
    app.to_label.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")

    app.to_entry = customtkinter.CTkOptionMenu(app.booking_frame, values=[
        "Scranton Business Park",
        "Dunder Mifflin Inc.",
        "Schrute Farms",
        "Electric City Sign",
        "New Hampshire",
        "Connecticut",
        "Utica",
        "Coopers",
        "Vance Refrigeration",
        "Alfredo's Pizza Cafe",
        "Hooters"
        ])
    app.to_entry.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="w")

    app.book_button = customtkinter.CTkButton(app.booking_frame, text="Book", command=app.book_tickets)
    app.book_button.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 10), sticky="ew")

    app.available_trains_label = customtkinter.CTkLabel(app.booking_frame, text="Available Trains:")
    app.available_trains_label.grid(row=3, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")

    app.available_trains_listbox = tk.Listbox(app.booking_frame)
    app.available_trains_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=(5, 10), sticky="nsew")

    app.booking_frame.grid_columnconfigure(0, weight=1)
    app.booking_frame.grid_columnconfigure(1, weight=1)
    app.booking_frame.grid_columnconfigure(2, weight=1)
    app.booking_frame.grid_rowconfigure(4, weight=1)

def update_available_trains(app, event):
    from_location = app.from_entry.get()
    to_location = app.to_entry.get()

    trains = get_available_trains(from_location, to_location)

    app.available_trains_listbox.delete(0, tk.END)
    for train in trains:
        app.available_trains_listbox.insert(tk.END, train)

def get_available_trains(from_location, to_location):
    return [f"Train {i} from {from_location} to {to_location}" for i in range(1, 6)]

def book_tickets(app):
    selected_trains = app.available_trains_listbox.curselection()
    if not selected_trains:
        tkinter.messagebox.showwarning("No Selection", "Please select a train to book.")
        return

    selected_trains_list = [app.available_trains_listbox.get(i) for i in selected_trains]

    tkinter.messagebox.showinfo("Booking Successful", f"Tickets booked for: {', '.join(selected_trains_list)}")
    clear_booking_form(app)

def clear_booking_form(app):
    app.from_entry.set("")
    app.to_entry.set("")
    app.available_trains_listbox.delete(0, tk.END)

def other_features(app):
    tkinter.messagebox.showinfo("Feature", "This is a placeholder for features.")