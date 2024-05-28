import sys
sys.dont_write_bytecode = True

import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import Image
import CreateConnection
import LoginVerifier
import os

from GUI_ui import create_login_form_ui, update_appearance_mode, clear_main_content, clear_sidebar
from GUI_Authentication import login, update_sidebar_after_login, logout, register
from GUI_Booking import booking_page, update_available_trains, book_tickets, clear_booking_form, other_features

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    
    UserName = ""
    Routes = []
    
    def __init__(self):
        super().__init__()

        self.UserName = ""
        
        # configure window
        self.title("Train Booking System")
        self.geometry(f"{1100}x580")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        light_image_path = os.path.join(os.path.dirname(__file__), "1.png")
        dark_image_path = os.path.join(os.path.dirname(__file__), "2.png")
        my_image = customtkinter.CTkImage(light_image=Image.open(light_image_path),
                                          dark_image=Image.open(dark_image_path),
                                          size=(930, 580))

        self.image_label = customtkinter.CTkLabel(self, image=my_image, text="")
        self.image_label.grid(row=0, column=1, sticky="nsew")

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        create_login_form_ui(self)
        update_appearance_mode(self)
    
    def setUsername(self, value):
        self.UserName = value
        
    def getUsername(self):
        return self.UserName
    
    def setRoutes(self, value):
        self.Routes = value
        
    def getRoutes(self):
        return self.Routes.copy()

    def clear_sidebar(self):
        clear_sidebar(self)

    def clear_main_content(self):
        clear_main_content(self)

    def login(self):
        login(self)

    def update_sidebar_after_login(self, username):
        update_sidebar_after_login(self, username)

    def logout(self):
        logout(self)

    def register(self):
        register(self)

    def booking_page(self):
        booking_page(self)

    def update_available_trains(self, event):
        update_available_trains(self, event)

    def book_tickets(self):
        book_tickets(self)

    def clear_booking_form(self):
        clear_booking_form(self)

    def other_features(self):
        other_features(self)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()