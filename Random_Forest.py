from tkinter import *
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import csv
from tkinter import filedialog

root = Tk()
root.geometry('1370x700+0+0')
root.title('NMRL FBE')

header = Frame(root, width=1370, bd=4)
header.pack(side=TOP, fill=X)

def submit_path():
    global df, departments, X_train, X_test, y_train, y_test, dept_models
    
    # Load data from CSV
    df = pd.read_csv(file_path)
    
    # Extract years and department names
    years = df['Year']
    departments = df.columns[1:]  # Exclude the 'Year' column
    
    # Convert to numpy array for modeling
    X = np.array(years).reshape(-1, 1)  # Years as input feature
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, df.iloc[:, 1:], test_size=0.2, random_state=42)
    
    # Train a random forest regression model for each department
    dept_models = {}
    for dept in departments:
        y = df[dept]
        model = RandomForestRegressor(random_state=42)
        model.fit(X_train, y_train[dept])
        dept_models[dept] = model
    
    # Display a message or update UI after model training (optional)
    print("Models trained successfully.")

def predict_total_forecast(year):
    total_forecast = 0
    for dept, model in dept_models.items():
        # Predict forecasted amount for the given year using the model for each department
        forecast_amount = model.predict(np.array(year).reshape(-1, 1))[0]
        total_forecast += forecast_amount
    return total_forecast

def predict_dept_forecast(year):
    dept_forecasts = {}
    for dept, model in dept_models.items():
        forecast_amount = model.predict(np.array(year).reshape(-1, 1))[0]
        dept_forecasts[dept] = forecast_amount
    return dept_forecasts

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        content = [row for row in reader]
    return content

def browse_files():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        print(file_path)

Label(header, text='NMRL FBE', font=('Times New Roman', 36, 'bold'), fg='black', bg='orange', bd=6, relief='ridge').pack(side=TOP, fill=X)
body = Frame(root, width=1370, bd=6, bg='yellowgreen', relief='ridge')
body.pack(side=TOP, fill=X)

Label(body, text='Select dataset to predict:', font=('Times New Roman', 14, 'bold'), bg='yellowgreen', fg='black').pack(side=LEFT)
browse_button = Button(body, text="Browse Documents", command=browse_files)
browse_button.pack(side=LEFT)

Label(body, text='Enter required year:', font=('Times New Roman', 14, 'bold'), bg='yellowgreen', fg='black').pack(side=LEFT)
e2 = Entry(body, font=('Times New Roman', 14, 'normal'), bd=4)
e2.pack(side=LEFT, padx=20)

btn_frame = Frame(root, width=1370, bd=4)
btn_frame.pack(side=TOP)

sbt_btn = Button(btn_frame, text='Submit', width=15, bd=3, command=submit_path)
sbt_btn.pack(side=LEFT)

def display_forecasts():
    year_to_predict = int(e2.get())
    
    # Total forecast for the organization
    total_forecast = predict_total_forecast(year_to_predict)
    total_text = f'Total forecasted amount for the organization in {year_to_predict}: {total_forecast}'
    
    # Department-wise forecasts
    dept_forecasts = predict_dept_forecast(year_to_predict)
    dept_text = "\nDepartment-wise forecasts:\n"
    for dept, forecast in dept_forecasts.items():
        dept_text += f"{dept}: {forecast}\n"
    
    # Display results
    result_text = total_text + "\n" + dept_text
    output = Frame(root, width=1370, bd=6, bg='black')
    output.pack(side=TOP)
    Label(output, text=result_text, font=('Times New Roman', 14, 'bold'), fg='aqua', bg='black', bd=6, pady=10).pack(side=TOP)
    Button(output, text='Clear Result', width=15, bd=3, command=output.destroy).pack(side=TOP)

sbt_btn_display = Button(btn_frame, text='Display Forecasts', width=15, bd=3, command=display_forecasts)
sbt_btn_display.pack(side=LEFT)

mainloop()

