from tkinter import *
from io import StringIO
from tkinter import messagebox
from tkinter.ttk import Style
import sqlite3
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import os
import csv
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tkcalendar import Calendar
from tkcalendar import DateEntry
from datetime import datetime

conn=sqlite3.connect('login.db')

root=Tk()
root.geometry('410x285+450+170')
root.title('Login Window')

global department, bg_image , budget_head, z , val ,bal,carry,p_no,p_details,bal_update,exd_btn,ea,eb,bal_exist,check

check=0
ea=0
eb=0
p_no=''
p_details=''
z=0
val=0
bal=0
carry=0
bal_update = 0
bal_exist = 0
def nmrl_interface(department):
    '''root1=Toplevel(root)'''
    root1=Tk()
    root1.title('Interface')
    root1.geometry('975x325+180+200')

    
        
    # def load_image(image_path):
    #     try:
    #         image = Image.open(image_path)
    #         return image
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Unable to load image. Error: {e}")
    #         return None
    
    def submit():    
        root1.destroy()
        '''CODE FOR 3RD WINDOW I.E. ITEMWISE BREAKDOWNNH'''
        #global year_og,department
    
        #bal = balance (remaining amount) #val = forecasted / header amount
        def forecast_wali_window(p_no,p_details,val,bal):
            global balance ,g,bal_update,bal1,exd_btn,treeview
            
            bal1=bal
            print("Balance, Header ,",bal,val)
            a = submit_details(year, department) * 100000
            balance = float(a)
            
            root2 = Tk()
            root2.geometry('975x800+180+20')
            root2.title('Forecast Window')
            heera=Frame(root2,width=10)
            heera.place(x=0,y=500)
            def pasha():
                pass
            exd_btn=Button(heera,text='Add to budget',width=10,bd=3,command=pasha)
            '''BUDGET HEAD IS HERE'''
            bh = budget_head
            '''BUDGET HEAD IS HERE'''

            def load_image(image_path):
                try:
                    image = Image.open(image_path)
                    return image
                except Exception as e:
                    messagebox.showerror("Error", f"Unable to load image. Error: {e}")
                    return None

            def clear_input():
                e2.delete(0, END)
                e3.delete(0, END)
                e4.delete(0, END)

            def select_date():
                def set_date():
                    selected_date = cal.get_date()
                    # Convert selected date to dd/mm/yy format
                    day, month, year = selected_date.split('/')
                    formatted_date = f'{day}/{month}/{year[-2:]}'
                    e4.delete(0, END)  # Clear current content
                    e4.insert(0, formatted_date)
                    top.destroy()  # Close the calendar window after selection

                top = Toplevel(root2)
                current_date=datetime.now()
                # Create Calendar with dd/mm/yy format
                cal = Calendar(top, selectmode='day', year=current_date.year, month=current_date.month, day=current_date.day, date_pattern='dd/mm/yy')
                cal.pack(padx=10, pady=10)
                select_button = Button(top, text="Select Date", command=set_date)
                select_button.pack(pady=10)

            def back_btn():
                root2.destroy()
                nmrl_interface(department)

            

            def add_item():
                global balance,add_label,g,bal1,exd_btn,ea,eb,bal_exist,carry,bal_upd,bal_exist,bal_update,check
                
                print("Bal update inside add: ",bal_update)
                
                bal_upd=bal1
                #bal_upd=bal1*-1
                print("upd bal : ",bal1)
                
                    
                item_name = e2.get()
                amount = e3.get()
                expected_cashout = e4.get()
                print(item_name,amount,expected_cashout)

                a=  any(not char.isdigit() for char in amount)
                if a==True:
                    messagebox.showwarning("Input Error", "Please enter only numeric value in Amount.")
                    clear_input()
                    return
                    

                if item_name and amount and expected_cashout:
                    check+=1
                    amount = float(e3.get())
                    treeview.insert("", "end", values=(item_name, amount, expected_cashout))
                    print(treeview.item(treeview.selection()))
                    clear_input()
                else:
                    messagebox.showwarning("Input Error", "Please fill all fields before adding.")
                    clear_input()
                    return

                if g>1:   
                    add_label.destroy()

                if carry==0:
                    bal_exist=balance
                    print("existing bal: ",bal_exist)
                    carry+=1
                    
                
                balance = balance -amount

                
                def exceed():
                    res = messagebox.askyesno("Add to Budget","Do you really want to add exceeding amount in total budget,it will also store it into CSV.")
                    if res == False:
                        return 
                    if bal1<0:
                        val=bal_update+ea
                        bal=val
                        #root2.destroy()
                        #forecast_wali_window(p_no,p_details,val,bal)
                
                    else:
                        val=bal_exist+eb
                        bal=val
                        #root2.destroy()
                        #forecast_wali_window(p_no,p_details,val,bal)

                    if z==1:
                        file_path = f'data/{department}_forecast_{year_og}_Project_Revenue&_Capital.csv'
                        with open(file_path, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            
                            writer.writerow(["Item Name", "Amount", "Expected Cashout"])
        
                            for row in treeview.get_children():
                                values = treeview.item(row, 'values')
                                writer.writerow(values)
    
                            header_row=f'Project Number:{p_no}'
                            print(p_no)
                            print(p_details)
                            subheader_row=f'Project Details:{p_details}'
                            writer.writerow(["-----","-----","-----"])
                            writer.writerow(["Project","Number","Details"])
                            writer.writerow(["===>",p_no,p_details])
                            writer.writerow(["-----","-----","-----"])
                            writer.writerow(["Department","Total Balance","Year"])
                            writer.writerow([department,bal,year_og])
                        check=0
                        messagebox.showinfo("Success", f"Data has been saved to {file_path}")
                        root2.destroy()
                        nmrl_interface(department)
                        
                    else:
                        file_path = f'data/{department}_forecast_{year_og}_General_Revenue&_Capital.csv'
                        with open(file_path, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(["Item Name", "Amount", "Expected Cashout"])
        
                            for row in treeview.get_children():
                                values = treeview.item(row, 'values')
                                writer.writerow(values)
    
                            writer.writerow(["-----","-----","-----"])
                            writer.writerow(["Department","Total Balance","Year"])
                            writer.writerow([department,bal,year_og])
                        check=0
                        messagebox.showinfo("Success", f"Data has been saved to {file_path}")
                        root2.destroy()
                        nmrl_interface(department)
                    
                        

                g+=1
                print("before rem bal 146")
                if bal ==0:
                    #exd_btn.destroy()
                    if balance<0:
                        b=0
                        add_label=Label(balance_frame, text=f'Remaining Balance: {b}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                        add_label.grid(row=0,column=4)
                    else:
                        add_label=Label(balance_frame, text=f'Remaining Balance: {balance}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                        add_label.grid(row=0,column=4)
                        
                else:
                    #bal1 = bal1-amount
                    bal1 = bal1-amount
                    print(bal1)
                    if bal1 < 0:
                        c=0
                        add_label=Label(balance_frame, text=f'Remaining Balance: {c}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                        add_label.grid(row=0,column=4)
                    else :
                        #bal1 = bal1-amount
                        add_label=Label(balance_frame, text=f'Remaining Balance: {bal1}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                        add_label.grid(row=0,column=4)

                if (bal1<0 or balance<0):
                    if bal1<0:
                        ea=bal1*-1
                        print("Update YZ",ea)  
                        add_label=Label(balance_frame, text=f'Exceeding Amount: {ea}', font=('Times New Roman', 24, 'bold'),fg='red', bd=6)
                        add_label.grid(row=1,column=4)
                        exd_btn=Button(balance_frame,text='Add to budget',width=10,bd=3,command=exceed)
                        exd_btn.grid(row=1,column=6)
                    else:
                        eb=balance*-1
                        print("Normal YZ ",eb)
                        add_label=Label(balance_frame, text=f'Exceeding Amount: {eb}', font=('Times New Roman', 24, 'bold'),fg='red', bd=6)
                        add_label.grid(row=1,column=4)
                        exd_btn=Button(balance_frame,text='Add to budget',width=10,bd=3,command=exceed)
                        exd_btn.grid(row=1,column=6)

            def delete_item():
                global balance,add_label,g,bal1,exd_btn,amount,bal_upd,bal_exist,bal_update,ea,eb,check
            
                # Get selected item

                
                selected_item = treeview.selection()

                
                def exceed():
                    res = messagebox.askyesno("Add to Budget","Do you really want to add exceeding amount in total budget,it will also store it into CSV.")
                    if res == False:
                        return 
                    if bal1<0:
                        #val=bal_upd+ea
                        val = bal_update+ea
                        bal=val
                        #root2.destroy()
                        #forecast_wali_window(p_no,p_details,val,bal)
                        #nmrl(department)
                        
                    else:
                        val=bal_exist+eb
                        bal=val
                        #root2.destroy()
                        #forecast_wali_window(p_no,p_details,val,bal)
                    if z==1:
                        file_path = f'data/{department}_forecast_{year_og}_Project_Revenue&_Capital.csv'
                        with open(file_path, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            
                            writer.writerow(["Item Name", "Amount", "Expected Cashout"])
        
                            for row in treeview.get_children():
                                values = treeview.item(row, 'values')
                                writer.writerow(values)
    
                            header_row=f'Project Number:{p_no}'
                            print(p_no)
                            print(p_details)
                            subheader_row=f'Project Details:{p_details}'
                            writer.writerow(["-----","-----","-----"])
                            writer.writerow(["Project","Number","Details"])
                            writer.writerow(["===>",p_no,p_details])
                            writer.writerow(["-----","-----","-----"])
                            writer.writerow(["Department","Total Balance","Year"])
                            writer.writerow([department,bal,year_og])
                        check=0
                        messagebox.showinfo("Success", f"Data has been saved to {file_path}")
                        root2.destroy()
                        nmrl_interface(department)
                        
                    else:
                        file_path = f'data/{department}_forecast_{year_og}_General_Revenue&_Capital.csv'
                        with open(file_path, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(["Item Name", "Amount", "Expected Cashout"])
        
                            for row in treeview.get_children():
                                values = treeview.item(row, 'values')
                                writer.writerow(values)
    
                            writer.writerow(["-----","-----","-----"])
                            writer.writerow(["Department","Total Balance","Year"])
                            writer.writerow([department,bal,year_og])
                        check =0
                        messagebox.showinfo("Success", f"Data has been saved to {file_path}")
                        root2.destroy()
                        nmrl_interface(department)
                
                        
               
                if selected_item:
                    check-=1
                    items = treeview.item(selected_item)
                    print(items)
                    val = items['values']
                    print(val)
                    if val:
                        value_to_delete=float(val[1])
                    
                    balance=balance+value_to_delete
                    print("item to del",value_to_delete)
                    print("Exist bal after del: ",balance)
                    treeview.delete(selected_item)
                    #exd_btn.destroy()

                    if g>1:   
                        add_label.destroy()

    
                    
                    g+=1
                    if bal ==0:
                        if balance<0:
                            b=0
                            add_label=Label(balance_frame, text=f'Remaining Balance: {b}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                            add_label.grid(row=0,column=4)
                        else:
                            add_label=Label(balance_frame, text=f'Remaining Balance: {balance}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                            add_label.grid(row=0,column=4)
                        exd_btn.destroy()    
                    else:
                        #bal1 = bal1+amount
                        bal1 = bal1+value_to_delete
                        if bal1 < 0:
                            c=0
                            add_label=Label(balance_frame, text=f'Remaining Balance: {c}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                            add_label.grid(row=0,column=4)
                        else :
                            #bal1 = bal1-amount
                            add_label=Label(balance_frame, text=f'Remaining Balance: {bal1}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                            add_label.grid(row=0,column=4)
                        exd_btn.destroy()
                    if (bal1<0 or balance<0):
                        if bal1<0:
                            ea=bal1*-1
                            print(ea)
                            add_label=Label(balance_frame, text=f'Exceeding Amount: {ea}', font=('Times New Roman', 24, 'bold'),fg='red', bd=6)
                            add_label.grid(row=1,column=4)
                            exd_btn=Button(balance_frame,text='Add to budget',width=10,bd=3,command=exceed)
                            exd_btn.grid(row=1,column=6)
                        else:
                            eb=balance*-1
                            print(eb)
                            add_label=Label(balance_frame, text=f'Exceeding Amount: {eb}', font=('Times New Roman', 24, 'bold'),fg='red', bd=6)
                            add_label.grid(row=1,column=4)
                            exd_btn=Button(balance_frame,text='Add to budget',width=10,bd=3,command=exceed)
                            exd_btn.grid(row=1,column=6)
                        
                else:
                    messagebox.showwarning("Delete Error", "No item selected to delete.")

            def red_label():
                global e2,e3,e4
                Label(table, text='Budget Head', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=0)
                Label(table, text='Item Name', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=2)
                Label(table, text='Amount', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=4)
                Label(table, text='Expected Cashout', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=6)
    
                Label(table, text=budget_head, font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2, column=0)
    
                e2 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e2.grid(row=2, column=2)
                e3 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e3.grid(row=2, column=4)
                e4 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e4.grid(row=2, column=6)
    
                open_calendar_button = Button(table, text="Open Calendar", command=select_date)
                open_calendar_button.grid(row=2, column=8)

            def list_table():
                global treeview
                add_btn = Button(list_frame, text='Add', width=10, bd=3, command=add_item)
                add_btn.grid(row=0, column=0, padx=40, pady=10, sticky="w")
    
                delete_btn = Button(list_frame, text='Delete Selected', width=15, bd=3, command=delete_item)
                delete_btn.grid(row=0, column=1, padx=40, pady=10, sticky="w")
    
                submit_btn = Button(list_frame, text='Submit', width=10, bd=3, command=submit_data)
                submit_btn.grid(row=0, column=2, padx=40, pady=10, sticky="w")

                back_frame= Frame(root2, width=1370)
                back_frame.place(x=0, y=67)
                
                back = Button(back_frame, text='\u2190 Back', font=('Times New Roman', 12, 'bold'), width=15, bd=3, fg='blue', bg='white', command=back_btn)
                back.grid(row=0, column=3, padx=40, pady=10, sticky="w")
    
                # Treeview to display added items column-wise
                columns = ("Item Name", "Amount", "Expected Cashout")
                treeview = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode='browse')
                treeview.heading("Item Name", text="Item Name")
                treeview.heading("Amount", text="Amount")
                treeview.heading("Expected Cashout", text="Expected Cashout")
                treeview.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")
    
                # Adjust the column widths
                treeview.column("Item Name", width=200)
                treeview.column("Amount", width=100)
                treeview.column("Expected Cashout", width=150)
    
                # Create a scrollbar
                scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=treeview.yview)
                treeview.configure(yscroll=scrollbar.set)
                scrollbar.grid(row=1, column=4, sticky='ns')
    
                mainloop()
            
            def balance_update():
                global val,bal,add_label,check
                if check!=0:
                    messagebox.showerror("Error","You can only update balance when you have NOT added any item in the list!")
                    return

                def back_btn():
                    root4.destroy()
                    forecast_wali_window(p_no,p_details,val,bal)
                    #nmrl_interface(department)
                
                def new_forecast_label():
                    global bal_update
                    val=float(e_upd.get())
                    bal=val
                    bal_update = val #updated balance stored
                    print(bal_update)
                    root4.destroy()
                    forecast_wali_window(p_no,p_details,val,bal)
               
                root2.destroy()    
                root4 = Tk()
                root4.geometry('250x200+500+150')
                root4.title('Update Balance')
                header = Frame(root4, width=1370, bd=4)
                header.pack(side=TOP, fill=X)
                Label(header,text='Update Budget',font=('Times New Roman', 18, 'bold'), fg='black', bg='orange', bd=6, relief='ridge').pack(side=TOP, fill=X)
            
                input1_frame = Frame(root4, width=1370, bd=4)
                input1_frame.place(x=0, y=70)
                Label(input1_frame, text='Enter New Forecast Amount', font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=3,column=4)
                e_upd = Entry(input1_frame, font=('Times New Roman', 14, 'normal'), bd=4)
                e_upd.grid(row=4,column=4)
                
                bttn1_frame = Frame(root4, width=1370, bd=4)
                bttn1_frame.place(x=62, y=150)
                upd_button=Button(bttn1_frame, text='Submit', width=15,bd=3, command=new_forecast_label)
                upd_button.grid(row=5,column=4)

                back1_frame= Frame(root4, width=1370, bd=4)
                back1_frame.place(x=0,y=50)
                
                back = Button(back1_frame, text='\u2190', font=('Times New Roman', 8, 'bold'), width=2, fg='blue', bg='white', command=back_btn)
                back.grid(row=0,column=0)
                    
                
                
                
            def submit_data():
                global z,p_no,p_details,ea,eb,check
                # Create 'data' directory if it doesn't exist
                if ea!=0 or eb!=0:
                    messagebox.showerror("Submit Error", "Please press 'ADD TO BUDGET' button,it will automatically save your data and update budget in CSV.")
                    return
                    
                if check==0:
                    messagebox.showerror("Submit Error", "Please atleast Add one item row details.")
                    return
                    
                    
                
                if not os.path.exists('data'):
                    os.makedirs('data')

                # Define file path for CSV
                if z==1:
                    file_path = f'data/{department}_forecast_{year_og}_Project_Revenue&_Capital.csv'
                    with open(file_path, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        
                        writer.writerow(["Item Name", "Amount", "Expected Cashout"])
    
                        for row in treeview.get_children():
                            values = treeview.item(row, 'values')
                            writer.writerow(values)

                        header_row=f'Project Number:{p_no}'
                        print(p_no)
                        print(p_details)
                        subheader_row=f'Project Details:{p_details}'
                        writer.writerow(["-----","-----","-----"])
                        writer.writerow(["Project","Number","Details"])
                        writer.writerow(["===>",p_no,p_details])
                        writer.writerow(["-----","-----","-----"])
                        writer.writerow(["Department","Total Balance","Year"])
                        writer.writerow([department,bal_update,year_og])
                    check=0
                    messagebox.showinfo("Success", f"Data has been saved to {file_path}")
                    
                    root2.destroy()
                    nmrl_interface(department)
                    
                else:
                    file_path = f'data/{department}_forecast_{year_og}_General_Revenue&_Capital.csv'
                    with open(file_path, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Item Name", "Amount", "Expected Cashout"])
    
                        for row in treeview.get_children():
                            values = treeview.item(row, 'values')
                            writer.writerow(values)

                        writer.writerow(["-----","-----","-----"])
                        writer.writerow(["Department","Total Balance","Year"])
                        writer.writerow([department,bal_exist,year_og])
                    check=0
                    messagebox.showinfo("Success", f"Data has been saved to {file_path}")
                    root2.destroy()
                    nmrl_interface(department)

                # Write data to CSV
                
               
            # image_path = 'C:/Users/Administrator/Internship/nmrl_logo.jpg'
            # image1 = load_image(image_path)
            # if image1:
            #     image1 = image1.resize((100, 60), Image.LANCZOS)
            #     bg_image = ImageTk.PhotoImage(image1)

            #     # Create a canvas to place the image
            #     canvas = Canvas(root2, width=200, height=200)
            #     canvas.place(x=0, y=0, relwidth=1, relheight=1)
            #     canvas.create_image(50, 40, image=bg_image, anchor="center")

            header = Frame(root2, width=1370, bd=4, bg='orange')
            header.place(x=130,y=0)

            if val ==0:
                Label(header, text=f'{department} {year_og} Forecast Budget: {a:.2f}', font=('Times New Roman', 24, 'bold'), fg='black', bd=6).grid(row=0,column=0)
            else:
                Label(header, text=f'{department} {year_og} Forecast Budget: {val:.2f}', font=('Times New Roman', 24, 'bold'), fg='black', bd=6).grid(row=0,column=0)
                
            
            upd_button=Button(header, text='Update Balance', width=15,bd=3, command=balance_update)
            upd_button.grid(row=0,column=22)
            if budget_head=='Project Revenue/Capital':
                global z 
        
                z=1
                g=1
                input_frame = Frame(root2, width=1370, bd=4,relief='ridge')
                input_frame.place(x=0, y=170)
    
                number=p_no
                details=p_details
                balance_frame = Frame(root2, width=1370, bd=4)
                balance_frame.place(x=300, y=62)
                #balance=submit_details(year, department) * 100000
                add_label=Label(balance_frame,text='',font=('Times New Roman', 1, 'bold'),fg='white')
                add_label.grid(row=0,column=0)
                Label(input_frame,text=f'Project Number: {p_no}',font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=1,column=1)
                Label(input_frame,text=f'Project Details: {p_details}',font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=2,column=1)


    
                table = Frame(root2, width=1370, bd=4, relief='ridge')
                table.place(x=0, y=260)

                red_label()
                
                # Frame for the list display and buttons
                list_frame = Frame(root2, width=1370, bd=4, relief='ridge')
                list_frame.place(x=250, y=360)
    
                # Add, clear input fields, and submit buttons
                
                list_table()
            
            else:
                z=0
                input_frame = Frame(root2, width=1370, bd=4,relief='ridge')
                input_frame.place(x=0, y=120)
                g=1
                #number=p_no
                #details=p_details
                
                balance_frame = Frame(root2, width=1370, bd=4)
                balance_frame.place(x=250, y=80)
          
                add_label=Label(balance_frame,text='',font=('Times New Roman', 1, 'bold'),fg='white')
                add_label.grid(row=0,column=0)

                
                Label(input_frame,text='Itemwise Breakdown',font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=3,column=1)
    
                table = Frame(root2, width=1370, bd=4, relief='ridge')
                table.place(x=0, y=180)
    
                red_label()
    
                # Frame for the list display and buttons
                list_frame = Frame(root2, width=1370, bd=4, relief='ridge')
                list_frame.place(x=250, y=280)
    
                # Add, clear input fields, and submit buttons
                list_table()

        def submit_details(year,dept_inp):

            global df, departments, X_train, X_test, y_train, y_test, dept_models, dept_rf_models

            data={'FINANCIAL_YR': [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024], 
                'ACC': [2.0, 2.0, 2.0, 0.1, 0.3, 0.3, 0.3, 15.0, 5.0, 1.0, 5.0, 5.0, 1.0, 1.2, 7.0, 3.2, 2.0, 2.0, 2.0, 2.0], 
                'ADM': [2.0, 2.0, 2.0, 0.1, 0.3, 0.3, 0.3, 15.0, 7.1, 26.7, 5.0, 4.0, 12.25, 10.0, 9.0, 15.0, 14.0, 14.0, 14.0, 14.0], 
                'CER': [460.0, 460.0, 460.0, 521.0, 70.0, 5000.0, 14.0, 1171.9, 428.75, 692.7, 721.5, 411.6, 520.0, 545.5, 473.0, 758.0, 96.5, 343.5, 824.0, 1769.8], 
                'COM': [10.0, 10.0, 10.0, 21.0, 0.3, 0.3, 0.3, 50.0, 100.0, 225.0, 244.0, 1.0, 28.25, 15.0, 28.1, 50.0, 83.0, 26.0, 26.0, 26.0], 
                'EST': [1714.0, 1714.0, 1714.0, 1930.0, 50.0, 50.0, 50.0, 19315.0, 10352.0, 39114.92273, 22605.0, 22588.0, 10230.0, 9596.0, 8979.0, 6895.0, 3511.36, 1537.312, 18634.0, 18634.0], 
                'HND': [0.2, 0.2, 0.2, 0.15, 0.3, 0.3, 50.0, 0.2, 2.0, 0.3, 1.0, 4.0, 0.5, 2.44, 1.65, 1.5, 2.0, 2.0, 2.0, 2.0], 
                'MBE': [337.0, 337.0, 337.0, 264.5, 45.3, 45.3, 200.0, 389.8, 403.33, 284.15, 300.0, 427.0, 314.5, 500.0, 220.3, 101.1, 219.53, 11.0, 16.826, 16.0], 
                'MET': [7.1, 7.1, 175.0, 50.0, 45.0, 45.0, 32.0, 1717.0, 1569.75, 2365.0, 2575.5, 1654.0, 662.0, 519.8, 1237.0, 820.9, 1186.5, 147.7, 28.0, 28.0], 
                'MMG': [0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 50.0, 20.0, 20.0, 28.5, 43.0, 3.0, 20.0, 15.0, 25.0, 20.0, 20.0, 20.0, 20.0], 
                'MS0': [25.0, 25.0, 25.0, 0.1, 0.3, 0.3, 0.3, 0.5, 2.0, 11.0, 9.4, 55.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0], 
                'MTT': [0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 45.0, 55.0, 7.0, 50.0, 42.0, 60.0, 60.0, 32.0, 51.05, 50.0, 38.0, 38.0, 38.0], 
                'PNT': [366.4, 366.4, 366.4, 196.0, 35.0, 35.0, 35.0, 435.0, 156.75, 225.0, 110.5, 310.0, 737.0, 792.3, 367.0, 504.8, 653.77, 3178.0, 3178.0, 3178.0], 
                'POL': [330.9, 330.9, 330.9, 189.0, 1443.0, 1443.0, 1443.0, 1287.0, 727.05, 2070.0, 663.5, 1805.0, 3087.0, 1746.0, 1698.055, 667.4, 928.74, 150.99, 131.5, 8.0], 
                'QAE': [19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 3.33, 14.0, 9.0, 15.0, 20.0, 105.0, 35.0, 5.0003, 70.0, 2.5, 2.5, 2.5], 
                'TSO': [0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 5.0, 12.0, 10.0, 1.0, 10.0, 4.0, 10.0, 13.0, 13.0, 11.0, 11.0, 11.0, 11.0], 
                'VSG': [0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 6.0, 300.0, 373.4, 733.0, 600.0, 5.0, 5.0, 202.0, 14.0, 57.0, 5.0, 28.0, 123.0, 73.0], 
                'WEG': [0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 0.5, 1.5, 1.0, 1.5, 100.0, 100.0, 102.0, 297.0, 6.7, 5.0, 5.0, 10.0, 6.7], 
                'WLF': [1.0, 1.0, 1.0, 0.1, 0.5, 0.5, 0.5, 10.0, 3.0, 20.0, 18.0, 7.0, 7.0, 9.75, 10.25, 5.0, 15.25, 15.25, 15.25, 15.25]}
            

            # Convert the CSV string to a DataFrame
            df=pd.DataFrame(data)
            #df = pd.read_csv(StringIO(data))
            #print()

            #df = pd.read_csv('C:/Users/Administrator/Desktop/BUDGET_DATASET.csv')
            years = df['FINANCIAL_YR']
            departments = df.columns[1:]  # Exclude the 'Year' column
                    
            # Convert to numpy array for modeling
            X = np.array(years).reshape(-1, 1)  # Years as input feature
                    
            # Split data into training and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, df.iloc[:, 1:], test_size=0.2, random_state=42)
                    
            # Train both linear regression and random forest models for each department
            dept_models = {}
            dept_rf_models = {}
            for dept in departments:
                y = df[dept]
                lin_model = LinearRegression()
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                lin_model.fit(X_train, y_train[dept])
                rf_model.fit(X_train, y_train[dept])
                dept_models[dept] = lin_model
                dept_rf_models[dept] = rf_model

            
            dept_fore = 0
            for dept, model in dept_models.items():
                if dept == dept_inp:
                    rf_model = dept_rf_models[dept]
                    lin_pred = model.predict(np.array(year).reshape(-1, 1))[0]
                    rf_pred = rf_model.predict(np.array(year).reshape(-1, 1))[0]
                    forecast_amount = (lin_pred + rf_pred) / 2
                    dept_fore = round(forecast_amount, 2)
                    return dept_fore

        def project_details(year,department):
            #root3=Toplevel(root)
            root3=Tk()
            root3.geometry('400x350+450+100')
            root3.title('Project Information')
            
            def submit_project():
                global p_no, p_details
                p_no=e1.get()
                p_details=e2.get()
                root3.destroy()
                forecast_wali_window(p_no,p_details,val,bal)
                #submit_details(year,department)
            
            def clear_input():
                e1.delete(0,END)
                e2.delete(0,END)

            def back_btn():
                root3.destroy()
                #p_no=''
                #p_details=''
                nmrl_interface(department)
                
            header = Frame(root3, width=1370, bd=4)
            header.pack(side=TOP, fill=X)
            Label(header,text='Project Details',font=('Times New Roman', 28, 'bold'), fg='black', bg='orange', bd=6, relief='ridge').pack(side=TOP, fill=X)
            
            input_frame= Frame(root3, width=1370, bd=4)
            input_frame.place(x=20,y=100)
            
            Label(input_frame,text='Project No:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=0,column=2)
            e1 = Entry(input_frame, font=('Times New Roman', 14, 'normal'), bd=4)
            e1.grid(row=0,column=4)
            
            Label(input_frame,text='Project Details:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2,column=2)
            e2 = Entry(input_frame, font=('Times New Roman', 14, 'normal'), bd=4)
            e2.grid(row=2,column=4)
            
            btn_frame= Frame(root3, width=1370, bd=4)
            btn_frame.place(x=150,y=180)
            
            sbt_btn = Button(btn_frame, text='Submit', width=10, bd=3, command=submit_project)
            sbt_btn.grid(row=0,column=3)
            
            clear_btn = Button(btn_frame, text='Clear', width=10, bd=3, command=clear_input)
            clear_btn.grid(row=0,column=5)
            
            back1_frame= Frame(root3, width=1370, bd=4)
            back1_frame.place(x=0,y=65)
            
            back = Button(back1_frame, text='\u2190', font=('Times New Roman', 10, 'bold'), width=2, fg='blue', bg='white', command=back_btn)
            back.grid(row=0,column=0)  # Adjust padx and pady as needed
            
            mainloop()

        #def new():
            #pass
        year_og = year_var.get()
        year_str = year_og[0:4]
        budget_head = bh_var.get()

        if year_str=="" or budget_head=="":
            messagebox.showerror("Submit Error", f"Please select valid option")
            nmrl_interface(department)

        
        year = int(year_str)
        

        

        if budget_head=='Project Revenue/Capital':
            project_details(year,department)
        elif budget_head=='General Revenue/Capital':
            p_no=''
            p_details=''
            forecast_wali_window(p_no,p_details,val,bal)
        
        
    def clear_input():
        bh_var.set('')
        year_var.set('')

    def back_btn():
        root1.destroy()
        import NMRL_BFMS
        
    # image_path = 'C:/Users/Administrator/Internship/nmrl_logo.jpg'
    # image1 = load_image(image_path)
    # if image1:
    #     image1 = image1.resize((100, 60), Image.LANCZOS)
    #     bg_image = ImageTk.PhotoImage(image1)
    
    #      #Create a canvas to place the image
    #     canvas = Canvas(root1, width=200, height=200)
    #     canvas.place(x=0, y=0, relwidth=1, relheight=1)
    #     canvas.create_image(50, 40, image=bg_image, anchor="center")
       
    header = Frame(root1, width=1370, bd=4)
    header.pack(side=TOP,fill=X)
    dept_text=f'{department} division'
    Label(header,text='NMRL BUDGET FORECAST SYSTEM',font=('Times New Roman', 36, 'bold'), fg='black', bg='orange', bd=6, relief='ridge').pack(side=TOP,fill=X)
    Label(header,text=dept_text,font=('Times New Roman', 28, 'bold'), fg='blue', bd=6).pack(side=TOP,fill=X)
    
    input_frame= Frame(root1, width=1370, bd=4)
    input_frame.place(x=300,y=120)
    
    Label(input_frame,text='FBE Year:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=0,column=2)
    
    # Dropdown menu for department selection
    year_var = StringVar(root1)
    year=['2024-25','2025-26','2026-27','2027-28','2028-29','2029-30']
    year_var.set(year[0])  # Default department selection
    year_menu = OptionMenu(input_frame, year_var, *year)
    year_menu.config(width=25)
    style=Style()
    style.configure('TMenubutton',background='aqua')
    year_menu.grid(row=0,column=4)
    year_var.set('')
    
    
    Label(input_frame,text='Budget Head:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2,column=2)
    bh_var = StringVar(root1)
    bh=['General Revenue/Capital','Project Revenue/Capital']
    bh_var.set(bh[0])  # Default department selection
    bh_menu = OptionMenu(input_frame, bh_var, *bh)
    bh_menu.config(width=25)
    style=Style()
    style.configure('TMenubutton1',background='aqua')
    bh_menu.grid(row=2,column=4)
    
    bh_var.set('')
    
    
    btn_frame= Frame(root1, width=1370, bd=4)
    btn_frame.place(x=425,y=200)
    
    sbt_btn = Button(btn_frame, text='Submit', width=10, bd=3, command=submit)
    sbt_btn.grid(row=0,column=3)
    
    clear_btn = Button(btn_frame, text='Clear', width=10, bd=3, command=clear_input)
    clear_btn.grid(row=0,column=5)

    btn_frame1= Frame(root1, width=1370, bd=4)
    btn_frame1.place(x=465,y=240)
    
    logout = Button(btn_frame1, text='LogOut', font=('Times New Roman', 10, 'bold'), width=10, bd=3, fg='black', bg='red', command=back_btn)
    logout.grid(row=0,column=0)

    
    mainloop()
    
def submit():
    department = department_var.get()
    password = e2.get()
    root.destroy()

def clear_input():
    e2.delete(0,END)                                                                    
    department_var.set('')

def login():
    department = department_var.get()
    password = e2.get()

    # Connect to SQLite database
    conn = sqlite3.connect('login.db')
    c = conn.cursor()
    # Retrieve password from database for the selected department
    c.execute('SELECT PASSWORD FROM DEPT_LOGIN WHERE BRANCH_NAME=?', (department,))
    row = c.fetchone()

    if row:
        correct_password = row[0]
        if password == correct_password:
            messagebox.showinfo("Login Successful", f"Welcome to {department}!")
            root.destroy()
            nmrl_interface(department)
            
        else:
            messagebox.showerror("Login Error", "Incorrect password. Please try again.")
            e2.delete(0,END)
    else:
        messagebox.showerror("Login Error", "Department not found.")

    # Close database connection
    conn.close()

# HEADER FRAME
header = Frame(root, width=1370, bd=4)
header.pack(side=TOP, fill=X)
Label(header,text='Welcome',font=('Times New Roman', 28, 'bold'), fg='black', bg='orange', bd=6, relief='ridge').pack(side=TOP, fill=X)

# SUBHEADER FRAME                                                                               
subtitle = Frame(root, width=1370, bd=4)
subtitle.pack(side=TOP, fill=X)

Label(subtitle,text='Please Login',font=('Times New Roman', 20, 'normal'),bg='white', fg='blue', bd=6).pack(side=TOP, fill=X)

# INPUT FRAME

input_frame= Frame(root, width=1370, bd=4)
input_frame.place(x=40,y=120)

Label(input_frame,text='Department:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=0,column=2)

conn = sqlite3.connect('login.db')
c = conn.cursor()

# Retrieve department names from the database
c.execute('SELECT BRANCH_NAME FROM DEPT_LOGIN')
departments = [row[0] for row in c.fetchall()]

# Close database connection
conn.close()

# Dropdown menu for department selection
department_var = StringVar(root)
department_var.set(departments[0])  # Default department selection
department_menu = OptionMenu(input_frame, department_var, *departments)
department_menu.config(width=25)
style=Style()
style.configure('TMenubutton',background='aqua')
department_menu.grid(row=0,column=4)

Label(input_frame,text='Password:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2,column=2)
e2 = Entry(input_frame, font=('Times New Roman', 14, 'normal'), bd=4,show='*')
e2.grid(row=2,column=4)

btn_frame= Frame(root, width=1370, bd=4)
btn_frame.place(x=150,y=200)

sbt_btn = Button(btn_frame, text='Login', width=10, bd=3, command=login)
sbt_btn.grid(row=0,column=3)

clear_btn = Button(btn_frame, text='Clear', width=10, bd=3, command=clear_input)
clear_btn.grid(row=0,column=5)

mainloop()