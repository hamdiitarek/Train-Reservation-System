import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import Image
from my_sql import mySqlConnect 
from Controller import loginVerifierController as loginVerifier
from tkcalendar import Calendar

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Train Booking System")
        self.geometry(f"{1100}x{580}")

        my_image = customtkinter.CTkImage(light_image=Image.open("D:\\Users\\Hamdi\\Desktop\\EUI\\Semester 6\\CSE371 Database Systems\\Project\\Train Reservation System\\View\\Login.png"),
                                  dark_image=Image.open("D:\\Users\\Hamdi\\Desktop\\EUI\\Semester 6\\CSE371 Database Systems\\Project\\Train Reservation System\\View\\Login.png"),
                                  size=(1920, 1080))

        self.image_label = customtkinter.CTkLabel(self, image=my_image, text="")
        self.image_label.pack()

        # create login form
        self.username_label = customtkinter.CTkLabel(self, text="Username:")
        self.username_label.pack()

        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.pack()

        self.password_label = customtkinter.CTkLabel(self, text="Password:")
        self.password_label.pack()

        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_entry.pack()

        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = customtkinter.CTkButton(self, text="Register", command=self.register)
        self.register_button.pack()

        # center the login form
        self.username_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.username_entry.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
        self.password_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.password_entry.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
        self.login_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.register_button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

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
                    # Clear the login form
                    self.clear_login_form()
                    # Open a new view   
                    self.booking_page()
                    
                else:
                    tkinter.messagebox.showerror("Login Failed", "Incorrect password")
            else:
                tkinter.messagebox.showerror("Login Failed", "User not found")
        else:
            tkinter.messagebox.showerror("Database Error", "Failed to connect to the database")

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


    def create_login_form(self):
        # create login form
        self.username_label = customtkinter.CTkLabel(self, text="Username:")
        self.username_label.pack()

        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.pack()

        self.password_label = customtkinter.CTkLabel(self, text="Password:")
        self.password_label.pack()

        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_entry.pack()

        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack()

        # center the login form
        self.username_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.username_entry.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

    def clear_login_form(self):
            # Clear login form elements
            self.username_label.destroy()
            self.username_entry.destroy()
            self.password_label.destroy()
            self.password_entry.destroy()
            self.login_button.destroy()
            self.register_button.destroy()

    def booking_page(self):
        # create booking form

        self.departure_label = customtkinter.CTkLabel(self, text="Departure date:")
        self.departure_label.place(x=3, y=25)

        self.departure_entry = Calendar(self, selectmode="day", date_pattern="dd-mm-yyyy",borderwidth=0, bordercolor='white')
        self.departure_entry.pack()

        self.from_label = customtkinter.CTkLabel(self, text="From:")
        self.from_label.pack()

        self.from_entry = customtkinter.CTkOptionMenu(app, values=["option 1", "option 2"], command="")
        self.from_entry.pack()

        self.to_label = customtkinter.CTkLabel(self, text="To:")
        self.to_label.pack()

        self.to_entry = customtkinter.CTkOptionMenu(app, values=["option 1", "option 2"], command="")
        self.to_entry.pack()

        self.book_button = customtkinter.CTkButton(self, text="Book", command=self.book_tickets)
        
        #self.book_button.place(x=75, y=75)
        self.book_button.grid(row=6, column=6, padx = 10, pady = 10)

        #center the booking form
        self.from_label.place(relx=0.5, rely=0.4, anchor="center")
        self.from_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.to_label.place(relx=0.5, rely=0.5, anchor="center")
        self.to_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.departure_label.place(relx=0.5, rely=0.6, anchor="center")
        self.departure_entry.place(relx=0.5, rely=0.65, anchor="center")
        self.book_button.place(relx=0.5, rely=0.7, anchor="center")

    def book_tickets(self):
        from_location = self.from_entry.get()
        to_location = self.to_entry.get()
        departure_date = self.departure_entry.get()

        # Perform ticket booking logic

        # Show success message
        tkinter.messagebox.showinfo("Booking Successful", "Tickets booked successfully")

        # Clear the booking form
        self.clear_booking_form()

    def clear_booking_form(self):
        # Clear booking form elements
        self.from_label.destroy()
        self.from_entry.destroy()
        self.to_label.destroy()
        self.to_entry.destroy()
        self.departure_label.destroy()
        self.departure_entry.destroy()
        self.book_button.destroy()
if __name__ == "__main__":
    app = App()
    app.mainloop()
