import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import os
import tkinter.font as font
from tkinter import messagebox
from read_Image import Image_Read

my_w = None
img = None
bg = None
pathImage = None
def userInterfaces():
    global my_w ,img,bg
    my_w = tk.Tk()
    img =Image.open('image/background.png')
    bg = ImageTk.PhotoImage(img)
    my_w.config(bg="#26242f")  
    my_w.geometry("525x600")  # Size of the window 
    my_w.title('Computer Vision Project')

    l1 = tk.Label(my_w,image=bg,bg="#26242f")  
    l1.grid(row=1,column=1)
    myFont = font.Font(family='Helvetica', size=20, weight='bold')
    b1 = tk.Button(my_w, text='Click', width=15,bg="#404040",foreground="#FFFFFF",command = lambda:upload_file())
    # print(b1)
    b1['font'] = myFont
    b1.grid(row=2,column=1) 
    return my_w.mainloop() , pathImage

def upload_file():
    global pathImage

    # ('Jpg Files', '*.jpg'),('PNG files', '*.png'),
    f_types = [('all files', '.*')]
    filename = filedialog.askopenfilename(filetypes=f_types,title="Select Image",initialdir=os.getcwd())
    if  filename != '':
        # messagebox.showinfo("Message", "Image uploaded successfully.")
        pathImage = filename
        Image_Read.img= filename
        my_w.destroy()

# userInterfaces()
# my_w.mainloop()  # Keep the window open