import tkinter as tk
from tkinter import * 
from PIL import ImageTk, Image 
import time

def startup():

    w=Tk()

    #Using piece of code from old splash screen
    width_of_window = 427
    height_of_window = 250
    screen_width = w.winfo_screenwidth()
    screen_height = w.winfo_screenheight()
    x_coordinate = (screen_width/2)-(width_of_window/2)
    y_coordinate = (screen_height/2)-(height_of_window/2)
    w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
    #w.configure(bg='#ED1B76')
    w.overrideredirect(1) #for hiding titlebar

    tk.Frame(w, width=427, height=250, bg='#272727').place(x=0,y=0)
    label1=tk.Label(w, text='UGRA', fg='white', bg='#272727') #decorate it 
    label1.configure(font=("Game Of Squids", 24, "bold")) 
    label1.place(x=155,y=90)

    label2=tk.Label(w, text='Loading...', fg='white', bg='#272727') #decorate it 
    label2.configure(font=("Calibri", 11))
    label2.place(x=10,y=215)

    #making animation

    image_a=ImageTk.PhotoImage(Image.open(r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/c2.png'))
    image_b=ImageTk.PhotoImage(Image.open(r'C:/Users/DELL/Desktop/GUI_IIITNR/FFT PLOT/Icons/c1.png'))

    for i in range(5): #5loops
        l1=tk.Label(w, image=image_a, border=0, relief=SUNKEN).place(x=180, y=145)
        l2=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
        l3=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
        l4=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
        w.update_idletasks()
        time.sleep(0.3)

        l1=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
        l2=tk.Label(w, image=image_a, border=0, relief=SUNKEN).place(x=200, y=145)
        l3=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
        l4=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
        w.update_idletasks()
        time.sleep(0.3)

        l1=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
        l2=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
        l3=tk.Label(w, image=image_a, border=0, relief=SUNKEN).place(x=220, y=145)
        l4=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
        w.update_idletasks()
        time.sleep(0.3)

        l1=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
        l2=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
        l3=tk.Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
        l4=tk.Label(w, image=image_a, border=0, relief=SUNKEN).place(x=240, y=145)
        w.update_idletasks()
        time.sleep(0.3)

    w.destroy()