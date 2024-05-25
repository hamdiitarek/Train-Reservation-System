import customtkinter

def create_login_form_ui(app):
    app.clear_sidebar()

    app.username_label = customtkinter.CTkLabel(app.sidebar_frame, text="Username:")
    app.username_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

    app.username_entry = customtkinter.CTkEntry(app.sidebar_frame)
    app.username_entry.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")

    app.password_label = customtkinter.CTkLabel(app.sidebar_frame, text="Password:")
    app.password_label.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="w")

    app.password_entry = customtkinter.CTkEntry(app.sidebar_frame, show="*")
    app.password_entry.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="ew")

    app.login_button = customtkinter.CTkButton(app.sidebar_frame, text="Login", command=app.login)
    app.login_button.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="ew")

    app.register_button = customtkinter.CTkButton(app.sidebar_frame, text="Register", command=app.register)
    app.register_button.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="ew")

def update_appearance_mode(app):
    app.appearance_mode_label = customtkinter.CTkLabel(app.sidebar_frame, text="Appearance Mode:", anchor="w")
    app.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
    app.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(app.sidebar_frame, values=["System", "Light", "Dark"],
                                                                    command=app.change_appearance_mode_event)
    app.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))


def clear_sidebar(app):
    for widget in app.sidebar_frame.winfo_children():
        widget.destroy()

def clear_main_content(app):
    for widget in app.grid_slaves(row=0, column=1):
        widget.destroy()
