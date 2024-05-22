import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import Image
from my_sql import mySqlConnect 
from Controller import loginVerifierController as loginVerifier
from tkcalendar import Calendar
import os

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Train Booking System")
        self.geometry(f"{1100}x580")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        image_path = os.path.join(os.path.dirname(__file__), "Login.png")
        my_image = customtkinter.CTkImage(light_image=Image.open(image_path),
                                          dark_image=Image.open(image_path),
                                          size=(1920, 1080))

        self.image_label = customtkinter.CTkLabel(self, image=my_image, text="")
        self.image_label.grid(row=0, column=1, sticky="nsew")

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.create_login_form()
        self.update_appearance_mode()
    def update_appearance_mode(self):
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        

    def create_login_form(self):
        # create login form
        self.clear_sidebar()

        self.username_label = customtkinter.CTkLabel(self.sidebar_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.username_entry = customtkinter.CTkEntry(self.sidebar_frame)
        self.username_entry.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")

        self.password_label = customtkinter.CTkLabel(self.sidebar_frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="w")

        self.password_entry = customtkinter.CTkEntry(self.sidebar_frame, show="*")
        self.password_entry.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="ew")

        self.login_button = customtkinter.CTkButton(self.sidebar_frame, text="Login", command=self.login)
        self.login_button.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="ew")

        self.register_button = customtkinter.CTkButton(self.sidebar_frame, text="Register", command=self.register)
        self.register_button.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="ew")

    def clear_sidebar(self):
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

    def clear_main_content(self):
        for widget in self.grid_slaves(row=0, column=1):
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        mydb = mySqlConnect.ConnectToDatabase()
        if mydb:
            mycursor = mydb.cursor()
            sql = "SELECT password_hash, salt FROM users WHERE username = %s"
            val = (username,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()
            if result:
                stored_hashed_password, stored_salt = result
                if loginVerifier.verify_password(password, stored_hashed_password, stored_salt):
                    tkinter.messagebox.showinfo("Login Successful", "User logged in successfully")
                    # Update the sidebar with profile info
                    self.update_sidebar_after_login(username)
                    # Open the booking page
                    self.booking_page()
                else:
                    tkinter.messagebox.showerror("Login Failed", "Incorrect password")
            else:
                tkinter.messagebox.showerror("Login Failed", "User not found")
        else:
            tkinter.messagebox.showerror("Database Error", "Failed to connect to the database")

    def update_sidebar_after_login(self, username):
        self.clear_sidebar()

        self.profile_label = customtkinter.CTkLabel(self.sidebar_frame, text=f"Welcome, {username}")
        self.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")

        self.other_features_button = customtkinter.CTkButton(self.sidebar_frame, text="Other Features", command=self.other_features)
        self.other_features_button.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="ew")

    def logout(self):
        # Clear profile info and show login form
        self.create_login_form()
        #display the image in my_image
        self.image_labe
        
        # Clear the booking page or other main content
        self.clear_main_content()

    def register(self):
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()

        # Hash the password before storing it
        hashed_password, salt = loginVerifier.hash_password(new_password)

        # Insert the new user into the database
        if loginVerifier.create_user(new_username, hashed_password, salt):
            tkinter.messagebox.showinfo("Registration Successful", "User created successfully")
        else:
            tkinter.messagebox.showerror("Registration Failed", "Failed to create user")

    def booking_page(self):
        self.clear_main_content()

        self.booking_frame = customtkinter.CTkFrame(self)
        self.booking_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.departure_label = customtkinter.CTkLabel(self.booking_frame, text="Departure date:")
        self.departure_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.departure_entry = Calendar(self.booking_frame, selectmode="day", date_pattern="dd-mm-yyyy")
        self.departure_entry.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="w")

        self.from_label = customtkinter.CTkLabel(self.booking_frame, text="From:")
        self.from_label.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")

        self.from_entry = customtkinter.CTkOptionMenu(self.booking_frame, values=["option 1", "option 2"])
        self.from_entry.grid(row=1, column=1, padx=10, pady=(5, 10), sticky="w")

        self.to_label = customtkinter.CTkLabel(self.booking_frame, text="To:")
        self.to_label.grid(row=0, column=2, padx=10, pady=(10, 5), sticky="w")

        self.to_entry = customtkinter.CTkOptionMenu(self.booking_frame, values=["option 1", "option 2"])
        self.to_entry.grid(row=1, column=2, padx=10, pady=(5, 10), sticky="w")

        self.book_button = customtkinter.CTkButton(self.booking_frame, text="Book", command=self.book_tickets)
        self.book_button.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 10), sticky="ew")

        self.available_trains_label = customtkinter.CTkLabel(self.booking_frame, text="Available Trains:")
        self.available_trains_label.grid(row=3, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")

        self.available_trains_listbox = tk.Listbox(self.booking_frame)
        self.available_trains_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=(5, 10), sticky="nsew")

        self.booking_frame.grid_columnconfigure(0, weight=1)
        self.booking_frame.grid_columnconfigure(1, weight=1)
        self.booking_frame.grid_columnconfigure(2, weight=1)
        self.booking_frame.grid_rowconfigure(4, weight=1)

        # Bind the calendar selection to update the train list
        self.departure_entry.bind("<<CalendarSelected>>", self.update_available_trains)

    def update_available_trains(self, event):
        selected_date = self.departure_entry.get_date()
        from_location = self.from_entry.get()
        to_location = self.to_entry.get()

        # Query the database to get available trains for the selected date and locations
        trains = self.get_available_trains(selected_date, from_location, to_location)

        # Update the Listbox with the available trains
        self.available_trains_listbox.delete(0, tk.END)
        for train in trains:
            self.available_trains_listbox.insert(tk.END, train)

    def get_available_trains(self, date, from_location, to_location):
        # This function should query the database for available trains
        # For now, it returns a placeholder list of trains
        return [f"Train {i} from {from_location} to {to_location} on {date}" for i in range(1, 6)]

    def book_tickets(self):
        selected_trains = self.available_trains_listbox.curselection()
        if not selected_trains:
            tkinter.messagebox.showwarning("No Selection", "Please select a train to book.")
            return

        # Perform ticket booking logic for the selected trains
        selected_trains_list = [self.available_trains_listbox.get(i) for i in selected_trains]

        # Show success message
        tkinter.messagebox.showinfo("Booking Successful", f"Tickets booked for: {', '.join(selected_trains_list)}")

        # Clear the booking form
        self.clear_booking_form()

    def clear_booking_form(self):
        self.from_entry.set("")
        self.to_entry.set("")
        self.available_trains_listbox.delete(0, tk.END)

    def other_features(self):
        tkinter.messagebox.showinfo("Feature", "This is a placeholder for features.")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
