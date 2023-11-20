import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
import pickle
import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier
import att
import time
from datetime import datetime

class FaceRecognitionApp:
    def __init__(self, root):
        # Initialize the tkinter window
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("1080x730")

        # Create main frame and buttons
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=20)

        options = ["Register Faces", "Mark Attendance", "Check Name of Registered Faces", "Check Attendance", "Quit"]
        for option in options:
            btn = tk.Button(self.main_frame, text=option, width=30, height=2,
                            command=lambda opt=option: self.handle_option(opt))
            btn.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        self.faces_data = np.empty((0, 50*50), dtype=np.uint8)
        self.labels = []

    def handle_option(self, option):
        if option == "Register Faces":
            self.register_faces()
        elif option == "Mark Attendance":
            self.mark_attendance()
        elif option == "Check Name of Registered Faces":
            self.check_name()
        elif option == "Check Attendance":
            self.check_attendance()
        elif option == "Quit":
            self.quit_application()

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_input_dialog(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def quit_application(self):
        self.root.quit()

    def register_faces(self):
        name = self.show_input_dialog("Enter Your Name:")
        if name:
            video = cv2.VideoCapture(0)
            facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

            faces_data = []
            labels = []

            faces_count = 0
            while faces_count < 100:
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

    def mark_attendance(self):
        global output
        video = cv2.VideoCapture(0)
        facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

        with open('data/names.pkl', 'rb') as w:
            LABELS = pickle.load(w)
        with open('data/faces_data.pkl', 'rb') as f:
            FACES = pickle.load(f)

        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(FACES, LABELS)

        COL_NAMES = ['NAME', 'TIME']

        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                crop_img = gray[y:y + h, x:x + w]
                resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                output = knn.predict(resized_img)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
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
        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)
        self.result_label.config(text="\n".join(set(names)))

    def check_attendance(self):
        date = self.show_input_dialog("Enter the date (DD-MM-YYYY) to check attendance:")
        if date:
            file_path = f"Attendance/Attendance_{date}.csv"
            attendance_list = []
            if os.path.isfile(file_path):
                with open(file_path, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        attendance_list.append(f"Name: {row[0]}, Time: {row[1]}")
            else:
                attendance_list.append(f"No attendance data available for {date}")
            self.result_label.config(text="\n".join(attendance_list))

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
