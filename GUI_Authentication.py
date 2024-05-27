import sys
sys.dont_write_bytecode = True

import tkinter.messagebox
import customtkinter
import CreateConnection
import LoginVerifier
from GUI_ui import clear_main_content, clear_sidebar, create_login_form_ui

def login(app):
    username = app.username_entry.get()
    password = app.password_entry.get()
    
    if (len(username) == 0 or len(password) == 0):
        tkinter.messagebox.showinfo("incorrect info", "Username or password cannot be empty")
        return
        
    connection = CreateConnection.create()
    if connection:
        backEnd = connection.cursor()
        sql = "SELECT password_hash, salt FROM users WHERE username = %s"
        val = (username,)
        backEnd.execute(sql, val)
        result = backEnd.fetchone()
        if result:
            stored_hashed_password, stored_salt = result
            if LoginVerifier.verify_password(password, stored_hashed_password, stored_salt):
                tkinter.messagebox.showinfo("Login Successful", "User logged in successfully")
                app.setUsername(username)
                app.update_sidebar_after_login(username)
                app.booking_page()
            else:
                tkinter.messagebox.showerror("Login Failed", "Incorrect password")
        else:
            tkinter.messagebox.showerror("Login Failed", "User not found")
    else:
        tkinter.messagebox.showerror("Database Error", "Failed to connect to the database")

def update_sidebar_after_login(app, username):
    clear_sidebar(app)

    app.profile_label = customtkinter.CTkLabel(app.sidebar_frame, text=f"Welcome, {username}")
    app.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

    app.logout_button = customtkinter.CTkButton(app.sidebar_frame, text="Logout", command=app.logout)
    app.logout_button.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")

    app.other_features_button = customtkinter.CTkButton(app.sidebar_frame, text="Other Features", command=app.other_features)
    app.other_features_button.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="ew")

def logout(app):
    create_login_form_ui(app)
    clear_main_content(app)


def register(app):
    new_username = app.username_entry.get()
    new_password = app.password_entry.get()
    
    if (len(new_username) == 0 or len(new_password) == 0):
        tkinter.messagebox.showinfo("incorrect info", "Username or password cannot be empty")
        return
    

    connection = CreateConnection.create()
    backEnd = connection.cursor()
    sql = "SELECT password_hash, salt FROM users WHERE username = %s"
    val = (new_username,)
    backEnd.execute(sql, val)
    result = backEnd.fetchone()
    if result:
        stored_hashed_password, stored_salt = result
        if LoginVerifier.verify_password(new_password, stored_hashed_password, stored_salt):
            tkinter.messagebox.showinfo("Login Successful", "User logged in successfully")
            app.update_sidebar_after_login(new_username)
            app.booking_page()
        else:
            tkinter.messagebox.showerror("Login Failed", "User Already Exists.")
        return

    hashed_password, salt = LoginVerifier.hash_password(new_password)

    if LoginVerifier.create_user(new_username, hashed_password, salt):
        tkinter.messagebox.showinfo("Registration Successful", "User created successfully")
    else:
        tkinter.messagebox.showerror("Registration Failed", "Failed to create user")
