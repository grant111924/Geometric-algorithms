import matplotlib
import tkinter as tk
from ConvexHullClass_2D import ConvexHull


window =tk.Tk()
window.title("Project Visualization")
w = window.winfo_screenwidth()
h = window.winfo_screenheight()

window.geometry("%dx%d" %(w/4, h/5))
var =tk.IntVar()  
l=tk.Label(window,bg='yellow',width=50, text='Please select Convex Hull Data Space',font=("Courier",12))
l.pack()


def print_selection():
    if var.get() == 1:
        l.config(text="Convex hull 2D")
        ConvexHull().gift_wrapping()
    elif var.get() == 2:
        l.config(text="Convex hull 3D")
    elif var.get()== 3:
        l.config(text="Delaunay Triangulation")
         
tk.Radiobutton(window, text='Convex hull 2D',variable=var, value='1',font=("Courier",16),command=print_selection,indicatoron=0).pack(anchor="w")
tk.Radiobutton(window, text='Convex hull 3D',variable=var, value='2',font=("Courier",16),command=print_selection,indicatoron=0).pack(anchor="w")
tk.Radiobutton(window, text='Delaunay Triangulation',variable=var, value='3',font=("Courier",16),command=print_selection,indicatoron=0).pack(anchor="w")


window.mainloop()