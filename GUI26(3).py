# ****************************************************************************************************************************************

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import askokcancel,askretrycancel,askyesno
from tkcalendar import Calendar,DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import threading
import time
import requests
from PIL import ImageGrab,Image, ImageTk
import datetime
# from datetime import datetime
from reportlab.pdfgen import canvas
import cv2
import pandas as pd
import itertools
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
from statsmodels.tsa.arima.model import ARIMA



# Replace 'COM11' with the appropriate port for your sensors
SERIAL_PORT = 'COM11'
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def read_sensor_data(app):
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            # Assuming data format: "ECG: value, SpO2_level: value, Pulse: value"
            values = data.split(',')
            if len(values) == 3:
                # ppg_value=values[2].split('=')[1].strip()
                # app.ecg_value.set(ppg_value)
                app.ecg_value.set(values[2].split('=')[1].strip())
                ecg_value1 = (values[2].split('=')[1].strip())
                value = float(ecg_value1)
                datas["ECG"].append(value)
                datass["ECG"].append(value)


                app.SpO2_level_value.set(values[0].split('=')[1].strip())
                SpO2_level_value1 = (values[0].split('=')[1].strip())
                value_1 = float(SpO2_level_value1)
                datas["SpO2"].append(value_1)


                app.pulse_value.set(values[1].split('=')[1].strip())
                pulse_value1 = (values[1].split('=')[1].strip())
                value_2 = float(pulse_value1)
                datas["Heart_rate"].append(value_2)


                predicted_bp_systolic = estimate_blood_pressure_systolic(app.pulse_value)
                predicted_bp_diastolic = estimate_blood_pressure_diastolic(app.pulse_value)

                app.bp_value_systolic.set(predicted_bp_systolic)
                bp_value_systolic_value1 = (predicted_bp_systolic)
                value_3= float(bp_value_systolic_value1)
                datas["Sys_BP"].append(value_3)


                app.bp_value_diastolic.set(predicted_bp_diastolic)
                bp_value_diastolic_value1 = (predicted_bp_diastolic)
                value_4= float(bp_value_diastolic_value1)
                datas["Dia_BP"].append(value_4)

                timestamp = datetime.datetime.now().strftime("%M:%S")
                datas["Timestamp"].append(timestamp)

                if len(datass["ECG"]) > 100:  # Keep only the latest 100 data points
                    datass["ECG"].pop(0)

                
        time.sleep(0.01)


# Example training data (pulse rate, systolic BP, diastolic BP)
# This should be replaced with real data
pulse_rate = np.array([60,70,80,90,100,72,68,74,80,65,70,76,82,88,72,75,78,82,86,63,68,74,79,85,90,71,75,77,80,64,69,73,76,78,82,85,88,70,74,77,79,81,83,85,87,90,65,68,71,73,75,77,79,80,82]).reshape(-1, 1)
systolic_bp = np.array([110,120,130,140,150,120,118,122,126,115,116,124,130,134,120,122,128,132,136,110,118,124,130,136,140,118,122,126,128,112,116,120,124,126,130,134,138,118,122,126,130,132,134,136,138,140,114,116,118,120,122,124,126,128,130])
diastolic_bp = np.array([70,80,85,90,95,80,76,78,84,70,74,80,86,90,80,78,82,86,88,72,76,80,84,88,92,76,78,82,84,74,76,78,80,82,84,86,88,76,78,82,84,86,86,88,90,92,74,76,78,80,82,84,86,88,90])

# Train models
systolic_model = LinearRegression().fit(pulse_rate, systolic_bp)
diastolic_model = LinearRegression().fit(pulse_rate, diastolic_bp)

# Save models
joblib.dump(systolic_model, 'systolic_model.pkl')
joblib.dump(diastolic_model, 'diastolic_model.pkl')


# Load the pre-trained models
systolic_model = joblib.load('systolic_model.pkl')
diastolic_model = joblib.load('diastolic_model.pkl')

def estimate_blood_pressure_systolic(pulse_value):
    pulse_value_str=pulse_value.get()
    pulse_value_int=float(pulse_value_str)

    pulse_rate_sys_arr = np.array([[pulse_value_int]])
    systolic_bp = int(systolic_model.predict(pulse_rate_sys_arr)[0])
    return systolic_bp

def estimate_blood_pressure_diastolic(pulse_value):
    pulse_value_str=pulse_value.get()
    pulse_value_int=float(pulse_value_str)

    pulse_rate_dia_arr = np.array([[pulse_value_int]])
    diastolic_bp = int(diastolic_model.predict(pulse_rate_dia_arr)[0])
    return diastolic_bp

datass = {
    "ECG": []
}

datas = {
    "Timestamp": [],
    "ECG": [],
    "SpO2": [],
    "Heart_rate": [],
    "Sys_BP": [],
    "Dia_BP": []
}

class SensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("    IITJ                                                                                                                                                            ECG, PULSE RATE/HEART RATE, OXIMETER AND BLOOD PRESSURE CALCULATOR PROJECT")
        self.root.config(bg="#003B46")
        self.root.geometry("1515x790+0+0")
        self.root.iconbitmap("AIDE-logo.ico")
        self.root.attributes('-alpha', 1)

        self.data = {
            "Timestamp": [],
            "ECG": [],
            "SpO2": [],
            "Heart_rate": [],
            "Sys_BP": [],
            "Dia_BP": []
        }

        self.data1 = {
            "ECG": [],
            "SpO2": [],
            "Heart_rate": [],
            "Sys_BP": [],
            "Dia_BP": []
        }

        

        self.gender_var = tk.StringVar()
        self.var_entryname = tk.StringVar()
        self.var_age = tk.IntVar()
        self.ecg_value = tk.StringVar()
        self.SpO2_level_value = tk.StringVar()
        self.pulse_value = tk.StringVar()
        self.bp_value_systolic = tk.StringVar()
        self.bp_value_diastolic = tk.StringVar()
        

        self.create_widgets()
        threading.Thread(target=read_sensor_data, args=(self,), daemon=True).start()
        threading.Thread(target=self.collect_sensor_data, daemon=True).start()

    def create_widgets(self):

        self.img_logo=tk.PhotoImage(file="iitlogo.png")
        self.img_aide=tk.PhotoImage(file="AIDE.png")
        self.image_download=tk.PhotoImage(file="images.png")
        self.img_male=tk.PhotoImage(file="male.png")
        self.img_female=tk.PhotoImage(file="female.png")
        self.unknown_gender=tk.PhotoImage(file="unknown_gender.png")
        self.img_heartbeat=tk.PhotoImage(file="heartbeat.png")

        self.label_frame1=tk.LabelFrame(self.root,text="Patient Profile",labelanchor="n",bd=3,relief="sunken",bg="#2C7873")
        self.label_frame1.place(x=10,y=10,height=780,width=451)

        self.label_frame2=tk.LabelFrame(self.root,text="Patient ECG Report",labelanchor="ne",bg="#004445",bd=3,relief="sunken")
        self.label_frame2.place(x=458,y=10,height=780,width=637)

        self.label_frame8=tk.LabelFrame(self.root,text="Patient SpO2 Report",labelanchor="ne",bd=3,relief="sunken",bg="#004445")
        self.label_frame8.place(x=776,y=10,height=135,width=315)

        self.label_frame2=tk.LabelFrame(self.root,text="Patient  ECG  Report",labelanchor="ne",bg="#004445",bd=3,relief="sunken")
        self.label_frame2.place(x=776,y=135,height=135,width=315)

        self.label_frame10=tk.LabelFrame(self.root,text="Patient Pulse Report",labelanchor="ne",bg="#004445",bd=3,relief="sunken")
        self.label_frame10.place(x=462,y=10,height=135,width=318)

        self.label_frame3=tk.LabelFrame(self.root,text="Patient Data Entry",labelanchor="n",bd=3,relief="sunken",bg="#2C7873")
        self.label_frame3.place(x=1092,y=10,height=780,width=432)

        self.label_frame4=tk.LabelFrame(self.root,text="Data Entry Date",labelanchor="n",bd=3,relief="sunken",bg="#2C7873")
        self.label_frame4.place(x=1095,y=280,height=235,width=428)

        self.label_frame5=tk.LabelFrame(self.root,text="Patient Profile Image",labelanchor="ne",bd=3,relief="sunken",bg="#2C7873")
        self.label_frame5.place(x=12,y=558,height=228,width=446)

        self.label_frame6=tk.LabelFrame(self.root,text="IITJ Logo Image",labelanchor="nw",bd=3,relief="sunken",bg="#2C7873")
        self.label_frame6.place(x=1096,y=558,height=230,width=426)

        self.label_frame7=tk.LabelFrame(self.root,text="Report Date",labelanchor="n",bd=3,relief="sunken",bg="#2C7873")
        self.label_frame7.place(x=12,y=280,height=235,width=446)


        self.label_frame9=tk.LabelFrame(self.root,text="Patient  BP  Report",labelanchor="ne",bd=3,relief="sunken",bg="#004445")
        self.label_frame9.place(x=462,y=135,height=135,width=318)


        self.label = tk.Label(self.root,relief="sunken",image=self.img_heartbeat,bg="black",background="black")
        self.label.place(x=255,y=575)


        self.img_label=tk.Label(self.root, text="IITJ",relief="sunken",font=("DM Sans",19,"bold"),image=self.img_logo,bg="black",background="black")
        self.img_label.place(x=1324,y=575)

        self.img_label=tk.Label(self.root, text="IITJ",relief="sunken",font=("DM Sans",19,"bold"),image=self.img_aide,bg="black",background="black")
        self.img_label.place(x=1098,y=575)

        # self.img_label0=tk.Label(root, text="",relief="sunken",font=("Britannic Bold",19,"bold"),image=self.img_male,bg="black")
        # self.img_label0.place(x=1150,y=190)

        # self.img_label00=tk.Label(root, text="",relief="sunken",font=("Britannic Bold",19,"bold"),image=self.img_female,bg="black")
        # self.img_label00.place(x=1150,y=190) 

        self.img_label=tk.Label(self.root, text="",relief="sunken",font=("Britannic Bold",19,"bold"),image=self.unknown_gender,bg="black")
        self.img_label.place(x=12,y=575)     


        self.calendar=DateEntry(self.root,selectmode="day",year=2024,month=1,day=1,background="#07575B")
        self.calendar.place(x=1225,y=300,width=250)   

        self.date = tk.Label(self.root, text="Date of the Medical Test :",relief="groove",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.date.place(x=25,y=300)    

        self.date_label = tk.Label(self.root, text="",relief="sunken",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.date_label.place(x=25,y=400)

        self.name = tk.Label(self.root, text="Name:",relief="groove",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.name.place(x=1100,y=50)

        self.entry_name = tk.Entry(self.root,relief="raised",font=("DM Sans",19,"bold"),bd=6,textvariable=self.var_entryname,)
        self.entry_name.place(x=1195,y=50)

        self.g = tk.Label(self.root, text="",relief="sunken",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.g.place(x=25,y=50)

        self.g_name = tk.Label(self.root, text="(NAME)",font=(19),bg="#2C7873")
        self.g_name.place(x=345,y=53)

        self.gender = tk.Label(self.root, text="Gender:",relief="groove",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.gender.place(x=1100,y=110)

        self.download = tk.Label(self.root, text="Download here --> ",relief="ridge",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.download.place(x=670,y=600)

        # list_1=(("Male","M"),("Female","F"))
        
        # for i in list_1:
            
        #     self.radio_bt=tk.Radiobutton(root,text=i[0],value=i[1],variable=var_radio)
        #     self.radio_bt.deselect()
            
        #     # self.radio_bt.place(x=100,y=200)
        #     self.radio_bt.pack(side="left")

        # *************************  OR  ***********************************

        self.radio_bt=tk.Radiobutton(self.root,text="Male",value="M",variable=self.gender_var,background="#07575B")
        self.radio_bt.deselect()
        # self.radio_bt.place(x=100,y=200)
        self.radio_bt.place(x=1250,y=117)

        self.radio_bt1=tk.Radiobutton(self.root,text="Female",value="F",variable=self.gender_var,background="#07575B")
        self.radio_bt1.deselect()
        # self.radio_bt.place(x=100,y=200)
        self.radio_bt1.place(x=1350,y=117)  
            


        self.ga = tk.Label(self.root, text="",image="",relief="sunken",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.ga.place(x=25,y=110)

        self.ga_gender = tk.Label(self.root, text="(SEX [M/F])",font=(19),bg="#2C7873")
        self.ga_gender.place(x=345,y=113)

        self.age = tk.Label(self.root, text="Age:",relief="groove",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.age.place(x=1100,y=170)

        self.gan_age = tk.Label(self.root, text="(AGE)",font=(19),bg="#2C7873")
        self.gan_age.place(x=345,y=173)

        self.age_spinbox=ttk.Spinbox(self.root,from_=0,to=100,textvariable=self.var_age,wrap=True,width=10,background="#07575B")
        self.age_spinbox.place(x=1200,y=180)

        self.gan = tk.Label(self.root, text="",relief="sunken",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.gan.place(x=25,y=170)

        self.button=tk.Button(self.root,text="SUBMIT",cursor="hand2",fg="white",command=self.ganu_name,bd=6,relief="raised",bg="#011A27")
        self.button.place(x=1325,y=520)

        
        self.button1=tk.Button(self.root,text="DOWNLOAD PDF",cursor="hand2",fg="white",image=self.image_download,bg="#011A27",compound="top", command=self.save_screenshot,bd=6,relief="raised")#command=gandi_name
        self.button1.place(x=668,y=655)

        self.button3=tk.Button(self.root,text="DOWNLOAD Excel",cursor="hand2",fg="white",image=self.image_download,bg="#011A27",compound="top",command=self.save_data,bd=6,relief="raised")#command=gandi_name
        self.button3.place(x=790,y=655)


        self.button2=tk.Button(self.root,text="STOP / SAVE",cursor="hand2",fg="white",command=self.ganu,bd=6,relief="raised",bg="#011A27")
        self.button2.place(x=150,y=520)

        self.button4=tk.Button(self.root,text="DOWNLOAD PREDICTION",cursor="hand2",fg="white",command=self.download_predictions,bd=6,relief="raised",bg="#011A27")
        self.button4.place(x=925,y=604)

        self.button5 = tk.Button(self.root,text="COLLECT DATA",cursor="hand2",fg="white",command=self.collect_data,bd=6,relief="raised",bg="#011A27")
        self.button5.place(x=1405, y=520)

        self.button6 = tk.Button(self.root, text="ANALYZE ECG",cursor="hand2",fg="white",bd=6,relief="raised",bg="#011A27", command=self.analyze_ecg)
        self.button6.place(x=30,y=520)


        

        # self.button1=tk.Button(root,text="UBMIT",cursor="plus",fg="blue",command=)
        # self.button1.place(x=950,y=600)








        self.ecg_label = tk.Label(self.root, text="ECG -->",relief="groove",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.ecg_label.place(x=830,y=157)

        self.ecg_value_label = tk.Label(self.root, textvariable=self.ecg_value,relief="sunken",font=("DM Sans",14,"bold"),background="#07575B",bd=6,fg="white")
        self.ecg_value_label.place(x=830,y=220)

        self.SpO2_level_label = tk.Label(self.root, text="SpO2 Level -->",relief="groove",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.SpO2_level_label.place(x=830,y=32)

        self.SpO2_level_value_label = tk.Label(self.root, textvariable=self.SpO2_level_value,relief="sunken",font=("DM Sans",14,"bold"),background="#07575B",bd=6,fg="white")
        self.SpO2_level_value_label.place(x=830,y=94)

        self.pulse_label = tk.Label(self.root, text="Pulse Rate -->",relief="groove",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.pulse_label.place(x=520,y=32)

        self.pulse_value_label = tk.Label(self.root, textvariable=self.pulse_value,relief="sunken",font=("DM Sans",14,"bold"),background="#07575B",bd=6,fg="white")
        self.pulse_value_label.place(x=520,y=94)

        self.blood_pressure_label_ = tk.Label(self.root, text="Blood Pressure -->",relief="groove",font=("DM Sans",19,"bold"),background="#07575B",bd=6)
        self.blood_pressure_label_.place(x=520,y=157)

        self.blood_pressure_label_sys_value = tk.Label(self.root, textvariable=self.bp_value_systolic ,relief="sunken",font=("DM Sans",14,"bold"),background="#07575B",bd=6,fg="white")
        self.blood_pressure_label_sys_value.place(x=520,y=220)

        self.blood_pressure_label_dia_value = tk.Label(self.root, textvariable=self.bp_value_diastolic ,relief="sunken",font=("DM Sans",14,"bold"),background="#07575B",bd=6,fg="white")
        self.blood_pressure_label_dia_value.place(x=620,y=220)

        

        self.plot_figure = plt.Figure(figsize=(6, 3), dpi=100)
        self.ax = self.plot_figure.add_subplot(111)
        
        self.line, = self.ax.plot([], [])
        
        self.canvas = FigureCanvasTkAgg(self.plot_figure, master=root)
        self.canvas.get_tk_widget().place(x=475,y=282)


    def analyze_ecg(self):
        if len(datass["ECG"]) < 20:  # Check if there is enough data to analyze
            print("Not enough data to analyze")
            return

        # Fit ARIMA model
        model = ARIMA(datass["ECG"], order=(5, 1, 0))
        model_fit = model.fit()

        # Forecast future values
        forecast = model_fit.forecast(steps=60)
        future_predictions = forecast.tolist()

        self.ax.clear()
        self.ax.plot(datass["ECG"], label='Real-time ECG Data')
        self.ax.plot(range(len(datass["ECG"]), len(datass["ECG"]) + len(future_predictions)), future_predictions, label='Future ECG Predictions', linestyle='dotted')
        self.ax.set_title("ECG Data")
        # self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude in volts")

        self.ax.relim()      
        self.ax.autoscale_view()
        self.ax.legend()
        self.canvas.draw()    

    def collect_sensor_data(self):
        while True:
            timestamp = datetime.datetime.now().strftime("%M:%S")
            ecg = self.ecg_value.get()
            SpO2 = self.SpO2_level_value.get()
            heart_rate = self.pulse_value.get()
            sys_bp = self.bp_value_systolic.get()
            dia_bp = self.bp_value_diastolic.get()

            self.data["Timestamp"].append(timestamp)
            self.data["ECG"].append((ecg))
            self.data["SpO2"].append(SpO2)
            self.data["Heart_rate"].append(heart_rate)
            self.data["Sys_BP"].append(sys_bp)
            self.data["Dia_BP"].append(dia_bp)

            self.data1["ECG"].append(ecg)
            self.data1["SpO2"].append(SpO2)
            self.data1["Heart_rate"].append(heart_rate)
            self.data1["Sys_BP"].append(sys_bp)
            self.data1["Dia_BP"].append(dia_bp)

            
            # self.ax.set_ylim(19000, 60000)
            self.update_plot()
            time.sleep(1)

    def update_plot(self):
        self.ax.clear()
        self.ax.set_title("ECG Data")
        # self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude in volts")

        # self.ax.set_ylim([0, 50000])
        
        # self.ax.plot(self.data["Timestamp"], self.data["ECG"], label="ECG")
        self.ax.plot((datass["ECG"]), label="Real-time ECG Data")
        
        # self.ax.plot(self.data["Timestamp"], self.data["SpO2"], label="SpO2")
        # self.ax.plot(self.data["Timestamp"], self.data["Heart_rate"], label="Heart Rate")
        self.ax.legend(loc='upper right')

        # self.ax.set_xlim([0, 10])  # Set x-axis limit to show last 10 data points
        

        self.ax.relim()      
        self.ax.autoscale_view()
        self.canvas.draw()

    def collect_data(self):
        try:
            name = self.var_entryname.get()
            age = self.var_age.get()
            gender = self.gender_var.get()
            if not name or not age or not gender:
                messagebox.showerror("Error", "All fields are required")
                return

            profile_data = f"Name: {name}\nAge: {age}\nGender: {gender}"
            print(profile_data)
            messagebox.showinfo("Success", "Data Collected Successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_data(self):
        """Function to download the data as an Excel file."""
        try:
            # Convert the data dictionary to a pandas DataFrame
            df = pd.DataFrame(datas)

            # Save the DataFrame to an Excel file
            file_name = f"Medical_Report_Data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(file_name, index=False, engine='openpyxl')

            # Show a message box to inform the user
            messagebox.showinfo("Success", f"Data successfully saved to {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    def save_screenshot(self):
        try:
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            width = self.root.winfo_width()
            height = self.root.winfo_height()

            screenshot=ImageGrab.grab()
            screenshot_path="REPORT.png"
            screenshot.save(screenshot_path)
            pdf_path = "REPORT.pdf"
            c = canvas.Canvas(pdf_path)
            c.drawImage("REPORT.png", 0, 0, 595, 650)
            c.save()
            messagebox.showinfo("Success", f"MEDICAL REPORT downloaded successfully as {pdf_path}")
        except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def ganu(self):
            ans=askyesno(title="Confirmation",message="Do you want to save your MEDICAL REPORT !!")
            if ans==True:
                messagebox.showinfo(title="Saved", message=" Your MEDICAL REPORT saved successfully")
            else:
                messagebox.showerror("Error", "Your MEDICAL REPORT was not saved")

    def ganu_name(self):
            gender = self.gender_var.get()
            if gender == 'M':
                self.img_label.config(image=self.img_male)
            elif gender == 'F':
                self.img_label.config(image=self.img_female)

            var=self.calendar.get()
            
            self.g.config(text=self.var_entryname.get())   
            self.ga.config(text=self.gender_var.get())
            self.gan.config(text=str(self.var_age.get()))
            self.date_label.config(text=str(var))


    def download_predictions(self):
        try:
            # Save the initial data to CSV
            df0 = pd.DataFrame(datass)
            df1 = df0.dropna(how='all')
            df1.to_csv("initial_data.csv", index=False)

            # Perform predictions on the collected data
            predictions = self.predict_future_readings(df1)

            # Save predictions to CSV
            predictions.to_csv("predicted_data.csv", index=False)
            print("Prediction saved to predicted_data.csv")
            messagebox.showinfo(title="Success", message=" Your ECG REPORT was predicted and saved successfully as predicted_data.csv")

        except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")


    def predict_future_readings(self, df1):
        # Example prediction using linear regression on ECG values
        model = LinearRegression()
        X = np.arange(len(df1)).reshape(-1, 1)
        y = df1["ECG"].astype(float).values
        # # Replace empty strings with NaN
        # df1["ECG"] = df1["ECG"].replace('', np.nan)
        # # Drop rows with NaN values
        # df1.dropna(subset=["ECG"], inplace=True)
    
        # try:
        #     y = df1["ECG"].astype(float).values
        #     # Perform predictions or other operations with y
        # except ValueError as e:
        #     print(f"ValueError: {e}")

        # # y = df["ECG"].astype(float).values
        model.fit(X, y)
        
        # Predict the next 60 readings
        future_X = np.arange(len(df1), len(df1) + 60).reshape(-1, 1)
        future_predictions = model.predict(future_X)

        future_data = pd.DataFrame({
            "Time": range(len(df1), len(df1) + 60),
            "Predicted_ECG": future_predictions
        })

        return future_data                    

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()
