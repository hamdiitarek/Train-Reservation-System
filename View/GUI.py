import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image

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

        # center the login form
        self.username_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.username_entry.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
        self.password_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.password_entry.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
        self.login_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # perform login logic here
        # check if username and password are valid
        if username == "admin" and password == "password":
            tkinter.messagebox.showinfo("Login Successful", "Welcome, admin!")
        else:
            tkinter.messagebox.showerror("Login Failed", "Invalid username or password")


if __name__ == "__main__":
    app = App()
    app.mainloop()