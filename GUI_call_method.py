import matplotlib
import tkinter as tk
from ConvexHullClass_2D import ConvexHull
from ConvexHullClass_3D_2 import ConvexHull3D
from SmallestDiskClass import SmallestDisk
from DelaunayTriangulation import DelaunayTriangulation
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
        l.config(text="Smallest Circle Disk")
        SmallestDisk().min_circle()
    elif var.get()== 3:
        l.config(text="Convex hull 3D")
        ConvexHull3D().process()
    elif var.get() == 4:
        l.config(text="Delaunay Triangulation")
        DelaunayTriangulation().cal_delaunay_triangle()

tk.Radiobutton(window, text='Convex hull 2D',variable=var, value='1',font=("Courier",16),command=print_selection,indicatoron=0).pack(anchor="w")
tk.Radiobutton(window, text='Smallest Circle Disk',variable=var, value='2',font=("Courier",16),command=print_selection,indicatoron=0).pack(anchor="w")
tk.Radiobutton(window, text='Convex hull 3D',variable=var, value='3',font=("Courier",16),command=print_selection,indicatoron=0).pack(anchor="w")
tk.Radiobutton(window, text='Delaunay Triangulation',variable=var, value='4',font=("Courier",16),command=print_selection,indicatoron=0).pack(anchor="w")


window.mainloop()