import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog, FLAT
import cv2
import pickle
from PIL import Image, ImageTk
import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier
import time
from datetime import datetime
import csv
import firebase_admin
from firebase_admin import credentials, auth


cred = credentials.Certificate("authdemo-67785-firebase-adminsdk-up4co-757c47829e.json")
firebase_admin.initialize_app(cred)
firebase_api_key = 'AIzaSyBzuy6vXeDitBcqBkWMShWZ8fwElfnEyX0'

def authenticate(filename, username, password):
    if os.path.exists(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username and row[1] == password:
                    return True
    return False

class Register_face:
    def __init__(self, window, user_type):
        self.window = window
        self.window.geometry('1080x780')
        self.window.title("Face Recognition System")

        # Create main frame
        self.enter_frame = tk.Frame(self.window, bg='#040405', width=1080, height=780)
        self.enter_frame.place(x=0, y=0)

        self.side_image = tk.PhotoImage(file='q2.png')
        self.side_image_label = tk.Label(self.enter_frame, image=self.side_image, bg='#040405')
        self.side_image_label.place(x=300, y=0)

        self.username_label = tk.Label(self.enter_frame, text="Enter your name", bg="#ADD8E6", fg="#040405",
                                       font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = tk.Entry(self.enter_frame, highlightthickness=0, relief=tk.FLAT, bg="#ADD8E6",
                                       fg="#040405",
                                       font=("yu gothic ui ", 12, "bold"))
        self.username_entry.place(x=580, y=335, width=270)

        self.enter_img = ImageTk.PhotoImage(file='WW.png')
        self.enter = tk.Button(self.enter_frame, image=self.enter_img, bg='#98a65d', cursor="hand2",
                               borderwidth=0, background="#040405", activebackground="#040405",
                               command=self.register_face)
        self.enter.place(x=670, y=460, width=111, height=35)

        self.signup_img = ImageTk.PhotoImage(file='R.png')
        self.back_button_label = tk.Button(self.enter_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                           borderwidth=0, background="#040405", activebackground="#040405",
                                           command=self.go_back)
        self.back_button_label.place(x=670, y=530, width=111, height=35)

    def register_face(self):
        name = self.username_entry.get()
        if name:
            video = cv2.VideoCapture(0)
            facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

            faces_data = []
            labels = []

            faces_count = 0
            while faces_count < 300:
                ret, frame = video.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facedetect.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    crop_img = gray[y:y + h, x:x + w]
                    resized_img = cv2.resize(crop_img, (50, 50)).flatten()
                    faces_data.append(resized_img)
                    labels.append(name)
                    faces_count += 1
                    cv2.putText(frame, str(faces_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
                cv2.imshow("Frame", frame)
                k = cv2.waitKey(1)
                if k == ord('q') or faces_count == 100:
                    break
            video.release()
            cv2.destroyAllWindows()

            faces_data = np.array(faces_data)
            labels = [name] * len(faces_data)

            # Rest of your code for saving the data (same as before)
            self.save_data(faces_data, labels)

    def save_data(self, faces_data, labels):
        # Rest of your code for saving the data (same as before)
        if 'names.pkl' not in os.listdir('data/'):
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(labels, f)
        else:
            with open('data/names.pkl', 'rb') as f:
                names = pickle.load(f)
            names.extend(labels)
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)

        if 'faces_data.pkl' not in os.listdir('data/'):
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces_data, f)
        else:
            with open('data/faces_data.pkl', 'rb') as f:
                faces = pickle.load(f)
            faces = np.append(faces, faces_data, axis=0)
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces, f)

    def go_back(self):
        self.enter_frame.destroy()
        FaceRecognitionApp(self.window, 'names.pkl')
class FaceRecognitionApp:
    def __init__(self, window, user_type):
        self.window = window
        self.window.geometry('1080x780')
        self.window.title("Face Recognition System")

        # Create main frame
        self.main_frame = tk.Frame(self.window, bg='#040405', width=1080, height=780)
        self.main_frame.place(x=0, y=0)

        self.side_image = tk.PhotoImage(file='q2.png')
        self.side_image_label = tk.Label(self.main_frame, image=self.side_image, bg='#040405')
        self.side_image_label.place(x=300, y=0)

        self.btn_register_faces_img = tk.PhotoImage(file='C.png')
        self.btn_register_faces = tk.Button(self.main_frame, image=self.btn_register_faces_img, bg='#98a65d', cursor="hand2",
                                            borderwidth=0, background="#040405", activebackground="#040405", command=self.open_registration_face)
        self.btn_register_faces.place(relx=0.5, rely=0.5, anchor='center')

        self.btn_mark_attendance_img = tk.PhotoImage(file='ZZ.png')
        self.btn_mark_attendance = tk.Button(self.main_frame, image=self.btn_mark_attendance_img, bg='#98a65d', cursor="hand2",
                                             borderwidth=0, background="#040405", activebackground="#040405", command=self.mark_attendance)
        self.btn_mark_attendance.place(relx=0.5, rely=0.6, anchor='center')

        self.btn_check_names_img = tk.PhotoImage(file='X.png')
        self.btn_check_names = tk.Button(self.main_frame, image=self.btn_check_names_img, bg='#98a65d', cursor="hand2",
                                             borderwidth=0, background="#040405", activebackground="#040405", command=self.check_name)
        self.btn_check_names.place(relx=0.5, rely=0.7, anchor='center')

        # self.btn_check_attendance_img = tk.PhotoImage(file='VV.png')
        # self.btn_check_attendance = tk.Button(self.main_frame, image=self.btn_check_attendance_img, bg='#98a65d', cursor="hand2",
        #                                      borderwidth=0, background="#040405", activebackground="#040405", command=self.check_attendance)
        # self.btn_check_attendance.place(relx=0.5, rely=0.8, anchor='center')

        self.btn_quit_img = tk.PhotoImage(file='xc.png')
        self.btn_quit = tk.Button(self.main_frame, image=self.btn_quit_img, bg='#98a65d', cursor="hand2",
                                            borderwidth = 0, background="#040405", activebackground="#040405", command=self.quit_application)
        self.btn_quit.place(relx=0.5, rely=0.9, anchor='center')

        self.result_label = tk.Label(window, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        self.faces_data = np.empty((0, 50*50), dtype=np.uint8)
        self.labels = []

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_input_dialog(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def go_back_to_login(self):
        self.window.destroy()
        LoginPage(tk.Tk())

    def quit_application(self):
        self.go_back_to_login()

    def open_registration_face(self):
        self.clear_frame()
        # Pass the user_type parameter to the Register_face constructor
        Register_face(self.window, user_type='names.pkl')

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mark_attendance(self):
        global output
        video = cv2.VideoCapture(0)
        facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

        with open('data/names.pkl', 'rb') as w:
            LABELS = pickle.load(w)
        with open('data/faces_data.pkl', 'rb') as f:
            FACES = pickle.load(f)

        knn = KNeighborsClassifier(n_neighbors=10, weights='distance')  # Adjust parameters
        knn.fit(FACES, LABELS)

        COL_NAMES = ['NAME', 'TIME']

        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

            for (x, y, w, h) in faces:
                crop_img = gray[y:y + h, x:x + w]
                resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)

                # Use predict_proba to get confidence levels
                confidence = knn.predict_proba(resized_img)

                # Check if the max confidence is above a certain threshold (e.g., 0.95 for higher accuracy)
                if confidence.max() > 0.95:
                    output = knn.predict(resized_img)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            cv2.putText(frame, "Press 'o' for attendance", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("Frame", frame)
            k = cv2.waitKey(1)
            if k == ord('o'):
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                attendance = [str(output[0]), str(timestamp)]
                exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

                if exist:
                    with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(attendance)
                else:
                    with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        writer.writerow(attendance)
            if k == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

    def check_name(self):
        names_window = tk.Toplevel(self.window)
        names_window.title("Names List")

        # Create a Treeview widget for displaying names in tabular format
        names_tree = ttk.Treeview(names_window, columns=("Name"), show="headings")
        names_tree.heading("Name", text="Name")

        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)
            for name in set(names):
                names_tree.insert("", "end", values=(name,))

        names_tree.pack(padx=10, pady=10)

        # Create and add a Quit button to close the window
        quit_button = tk.Button(names_window, text="Quit", command=names_window.destroy)
        quit_button.pack(pady=10)

    # def check_attendance(self):
    #     date = self.show_input_dialog("Enter the date (DD-MM-YYYY) to check attendance:")
    #     if date:
    #         # Assuming the date is used as a key in the Firebase database
    #         attendance_data_ref = db.reference(f'/attendance/{date}')
    #
    #         # Retrieve the attendance data for the given date
    #         attendance_data = attendance_data_ref.get()
    #
    #         if attendance_data:
    #             # Create a CSV string for the attendance data
    #             csv_data = "Name,Time\n"
    #             for name, timestamp in attendance_data.items():
    #                 csv_data += f"{name},{timestamp}\n"
    #
    #             # Save the CSV data to a file
    #             file_path = f"Attendance_{date}.csv"
    #             with open(file_path, 'w') as csv_file:
    #                 csv_file.write(csv_data)
    #
    #             self.result_label.config(text=f"Attendance data for {date} saved to {file_path}")
    #         else:
    #             self.result_label.config(text=f"No attendance data available for {date}")
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
        web_api_key = 'AIzaSyCTKaq-I8ek-zYIKFvybB-xrg3OXEsf42Y'

        email = self.username_entry.get()
        password = self.password_entry.get()

        try:
            user = auth.create_user(
                email=email,
                password=password,
                email_verified=True,  # Set to True to mark the email as verified
                display_name="Optional Display Name"
            )
            messagebox.showinfo("User created successfully:", user.uid)
        except ValueError as ve:
            messagebox.showerror("Invalid input", str(ve))
        except auth.EmailAlreadyExistsError:
            messagebox.showerror("Error", "Email already exists. User creation failed.")
        except auth.WeakPasswordError:
            messagebox.showerror("Error", "Weak password. Strong password needed for security.")
            # Add a label below the password field to indicate the need for a strong password
            self.strong_password_label = tk.Label(self.reg_frame, text="Type a strong password", bg="#040405", fg="red",
                                                  font=("yu gothic ui", 10, "italic"))
            self.strong_password_label.place(x=580, y=450)
        except Exception as e:
            messagebox.showerror("Error", f"User creation failed. An error occurred: {str(e)}")

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
        web_api_key = 'AIzaSyCTKaq-I8ek-zYIKFvybB-xrg3OXEsf42Y'

        email = self.username_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return False

        try:
            user = auth.get_user_by_email(email)
            auth.sign_in_with_email_and_password(email, password)
            self.open_face_recognition("Teacher")
            return True
        except auth.UserNotFoundError:
            messagebox.showerror("Login Failed", "User not found. Login failed.")
        except auth.InvalidPasswordError:
            messagebox.showerror("Login Failed", "Invalid password. Login failed.")
        except auth.AuthError as e:
            messagebox.showerror("Login Failed", f"Login failed. An error occurred: {str(e)}")
        return False

    def open_face_recognition(self, user_type):
        self.clear_frame()
        FaceRecognitionApp(self.window, user_type)

    def clear_frame(self):
        for widget in self.lgn_frame.winfo_children():
            widget.destroy()

    def open_registration_page(self):
        self.clear_frame()
        RegistrationPage(self.window, "teachers.csv")


def main():
    window = tk.Tk()
    LoginPage(window)
    window.mainloop()

if __name__ == '__main__':
    main()
