import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk





window =tk.Tk()
window.title("Convex Hull 2D and 3D Visualization")
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry("%dx%d" %(w, h))

var =tk.StringVar()
l=tk.Label(window,bg='yellow',width=200, text='Please select Convex Hull Data Space',font=("Courier",30))
l.pack()
def print_selection():
    l.config(text='Convex Hull ' + var.get())
            
r1 = tk.Radiobutton(window, text='Convex hull 2D',variable=var, value='2D',font=("Courier",16),command=print_selection).pack(anchor="w")
r2 = tk.Radiobutton(window, text='Convex hull 3D',variable=var, value='3D',font=("Courier",16),command=print_selection).pack(anchor="w")

window.mainloop()