import tkinter as tk
from tkinter import messagebox, FLAT
from PIL import Image, ImageTk
import os
import csv
def authenticate(filename, username, password):
    if os.path.exists(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username and row[1] == password:
                    return True
    return False

class RegistrationPage:
    def __init__(self, window, filename):
        self.window = window
        self.window.geometry('950x600')
        self.window.title('Login Page')

        self.reg_frame = tk.Frame(self.window, bg='#040405', width=950, height=600)
        self.reg_frame.place(x=0, y=0)

        self.txt = "FACIAL RECOGNITION SYSTEM"
        self.heading = tk.Label(self.reg_frame, text=self.txt, font=('yu gothic ui', 30, "bold"), bg="#040405",
                                fg='white',
                                bd=4,
                                relief=FLAT)
        self.heading.place(x=100, y=30, width=700, height=40)

        self.side_image = Image.open('q2.png')
        side_photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = tk.Label(self.reg_frame, image=side_photo, bg='#040405')
        self.side_image_label.image = side_photo
        self.side_image_label.place(x=5, y=100)

        self.sign_in_image = Image.open('hyy.png')
        sign_in_photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = tk.Label(self.reg_frame, image=sign_in_photo, bg='#040405')
        self.sign_in_image_label.image = sign_in_photo
        self.sign_in_image_label.place(x=640, y=130)

        self.sign_in_label = tk.Label(self.reg_frame, text="register", bg="#040405", fg="white",
                                      font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=670, y=240)

        self.username_label = tk.Label(self.reg_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                       font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = tk.Entry(self.reg_frame, highlightthickness=0, relief=tk.FLAT, bg="#040405", fg="#6b6a69",
                                       font=("yu gothic ui ", 12, "bold"))
        self.username_entry.place(x=580, y=335, width=270)

        self.username_icon = Image.open('username_icon.png')
        username_icon_photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = tk.Label(self.reg_frame, image=username_icon_photo, bg='#040405')
        self.username_icon_label.image = username_icon_photo
        self.username_icon_label.place(x=550, y=332)

        self.password_label = tk.Label(self.reg_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                       font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = tk.Entry(self.reg_frame, highlightthickness=0, relief=tk.FLAT, bg="#040405", fg="#6b6a69",
                                       font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=580, y=416, width=244)

        self.password_icon = Image.open('password_icon.png')
        password_icon_photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = tk.Label(self.reg_frame, image=password_icon_photo, bg='#040405')
        self.password_icon_label.image = password_icon_photo
        self.password_icon_label.place(x=550, y=414)

        self.lgn_img = ImageTk.PhotoImage(file='T.png')
        self.login = tk.Button(self.reg_frame, image=self.lgn_img, bg='#98a65d', cursor="hand2",
                                             borderwidth=0, background="#040405", activebackground="#040405",
                               command=self.register_user)
        self.login.place(x=670, y=460, width=111, height=35)

        self.signup_img = ImageTk.PhotoImage(file='R.png')
        self.back_button_label = tk.Button(self.reg_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                             borderwidth=0, background="#040405", activebackground="#040405",
                                             command=self.go_back)
        self.back_button_label.place(x=670, y=530, width=111, height=35)

        self.filename = filename

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if not os.path.exists(self.filename):
                with open(self.filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Username", "Password"])
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password])
                messagebox.showinfo("Registration Successful", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username and password cannot be empty!")

    def go_back(self):
        self.reg_frame.destroy()
        LoginPage(self.window)

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('950x600')
        self.window.title('Login Page')

        self.lgn_frame = tk.Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=0, y=0)

        self.txt = "FACIAL RECOGNITION SYSTEM"
        self.heading = tk.Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 30, "bold"), bg="#040405",
                                fg='white', bd=4, relief=FLAT)
        self.heading.place(x=100, y=30, width=700, height=40)

        self.side_image = Image.open('q2.png')
        side_photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = tk.Label(self.lgn_frame, image=side_photo, bg='#040405')
        self.side_image_label.image = side_photo
        self.side_image_label.place(x=5, y=100)

        self.sign_in_image = Image.open('hyy.png')
        sign_in_photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = tk.Label(self.lgn_frame, image=sign_in_photo, bg='#040405')
        self.sign_in_image_label.image = sign_in_photo
        self.sign_in_image_label.place(x=640, y=130)

        self.sign_in_label = tk.Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                      font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=670, y=240)

        self.username_label = tk.Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                       font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = tk.Entry(self.lgn_frame, highlightthickness=0, relief=tk.FLAT, bg="#040405", fg="#6b6a69",
                                       font=("yu gothic ui ", 12, "bold"))
        self.username_entry.place(x=580, y=335, width=270)

        self.username_icon = Image.open('username_icon.png')
        username_icon_photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = tk.Label(self.lgn_frame, image=username_icon_photo, bg='#040405')
        self.username_icon_label.image = username_icon_photo
        self.username_icon_label.place(x=550, y=332)

        self.lgn_img = ImageTk.PhotoImage(file='WW.png')
        self.login = tk.Button(self.lgn_frame, image=self.lgn_img, bg='#98a65d', cursor="hand2",
                               borderwidth=0, background="#040405", activebackground="#040405",
                               command=self.validate_login)
        self.login.place(x=670, y=460, width=111, height=35)

        self.signup_img = ImageTk.PhotoImage(file='Y.png')
        self.signup_button_label = tk.Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                             borderwidth=0, background="#040405", activebackground="#040405",
                                             command=self.open_registration_page)
        self.signup_button_label.place(x=670, y=530, width=111, height=35)

        self.password_label = tk.Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                       font=("yu gothic ui", 15, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = tk.Entry(self.lgn_frame, highlightthickness=0, relief=tk.FLAT, bg="#040405", fg="#6b6a69",
                                       font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=580, y=416, width=270)

        self.password_icon = Image.open('password_icon.png')
        password_icon_photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = tk.Label(self.lgn_frame, image=password_icon_photo, bg='#040405')
        self.password_icon_label.image = password_icon_photo
        self.password_icon_label.place(x=550, y=414)

        self.show_image = ImageTk.PhotoImage(file='show.png')
        self.hide_image = ImageTk.PhotoImage(file='hide.png')
        self.show_button = tk.Button(self.lgn_frame, image=self.show_image, command=self.show_hide_password,
                                     relief=tk.FLAT, activebackground="white", borderwidth=0, background="white",
                                     cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show_hide_password(self):
        if self.password_entry.cget('show') == '':
            self.password_entry.config(show='*')
            self.show_button.config(image=self.show_image)
        else:
            self.password_entry.config(show='')
            self.show_button.config(image=self.hide_image)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if authenticate("students.csv", username, password):
            self.show_welcome_page("Student")
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials!")

    def show_welcome_page(self, user_type):
        self.clear_frame()
        welcome_label = tk.Label(self.lgn_frame, text=f"Welcome, {user_type}!", font=("Arial", 15, "bold"), bg="#040405", fg="white")
        welcome_label.place(x=300, y=150)

    def clear_frame(self):
        for widget in self.lgn_frame.winfo_children():
            widget.destroy()

    def open_registration_page(self):
        self.clear_frame()
        RegistrationPage(self.window, "students.csv")
def main():
    window = tk.Tk()
    LoginPage(window)
    window.mainloop()

if __name__ == '__main__':
    main()
