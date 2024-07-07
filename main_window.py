from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


def button1_command():
    # Code to call another Python file
    root.destroy()
    import Modified_Gui

def button2_command():
    # Code to call another Python file
    pass

def button3_command():
    # Code to call another Python file
    pass

def load_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load image. Error: {e}")
        return None

# Initialize main window
root = Tk()
root.title("NMRL Interface")
root.geometry("1370x700")

# Load the image
image_path = 'C:/Users/gaura/Desktop/NMRL/nmrl_logo.jpg'
image = load_image(image_path)
if image:
    image = image.resize((300, 300), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)

    # Create a canvas to place the image
    canvas = Canvas(root, width=1370, height=700)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.create_image(685, 350, image=bg_image, anchor="center")

# Create header frame
header_frame = Frame(root, bg="orange", height=50,bd=4,relief=RIDGE)
header_frame.pack(fill="x")

header_label = Label(header_frame, text="NMRL INTERFACE", font=("Arial", 24,'bold'), fg="black",bg='orange')
header_label.pack(pady=10)

select_frame = Frame(root, bg="white", height=50,bd=4,relief=RIDGE)
select_frame.pack(fill="x")

select_label = Label(select_frame, text="SELECT REQUIRED FUNCTION", font=("Arial", 24,'bold'), fg="blue",bg='white')
select_label.pack(pady=10)


# Create button frame
button_frame = Frame(root, bg="green", height=100,bd=4,relief=RIDGE)
button_frame.pack(fill="x")

# Add buttons
button1 = ttk.Button(button_frame, text="Budget Forecast", command=button1_command)
button1.pack(side="left", expand=True, padx=20,pady=10)

button2 = ttk.Button(button_frame, text="Button 2", command=button2_command)
button2.pack(side="left", expand=True, padx=20,pady=10)

button3 = ttk.Button(button_frame, text="Button 3", command=button3_command)
button3.pack(side="left", expand=True, padx=20,pady=10)

# Start the Tkinter event loop
root.mainloop()