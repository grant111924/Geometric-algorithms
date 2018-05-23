#-*- coding: utf-8 -*-
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk


"""window =tk.Tk()
window.title("Convex Hull 2D and 3D Visualization")
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry("%dx%d" %(w, h))

var =tk.StringVar()
l=tk.Label(window,bg='yellow',width=200, text='Please select Convex Hull Data Space',font=("Courier",30))
l.pack()
def print_selection():
    l.config(text='Convex Hull ' + var.get())
            
#r1 = tk.Radiobutton(window, text='Convex hull 2D',variable=var, value='2D',font=("Courier",16),command=print_selection).pack(anchor="w")
#r2 = tk.Radiobutton(window, text='Convex hull 3D',variable=var, value='3D',font=("Courier",16),command=print_selection).pack(anchor="w")

    """
    
class GUI:
    def __init__ (self,window):
        self.window=window
        self.window.title("Convex Hull 2D and 3D Visualization")
        self.window_H=self.window.winfo_screenheight()
        self.window_W=self.window.winfo_screenwidth()
        self.window.geometry("%dx%d"%(self.window_W,self.window_H))
        self.var =tk.StringVar()
        self.l=tk.Label(window,bg='yellow',width=200, text='Please select Convex Hull Data Space',font=("Courier",30))
        self.l.pack()
    def print_selection(self):
        self.l.config(text='Convex Hull ' + self.var.get())
        if self.var.get() == "2D": 
            print("2D")
            fig = Figure()
            fig.clear()
            self.data=generate_data(0,20,(100,2))
            self.gift_wrapping(self.data,fig)
        elif self.var.get()=="3D":    
            print("3D")
            self.data=generate_data(0,20,(50,3))
    def add_radiobtn(self):
        self.r1 = tk.Radiobutton(window, text='Convex hull 2D',variable=self.var, value='2D',font=("Courier",16),command=self.print_selection).pack(anchor="w")
        self.r2 = tk.Radiobutton(window, text='Convex hull 3D',variable=self.var, value='3D',font=("Courier",16),command=self.print_selection).pack(anchor="w")

        
    def gift_wrapping(self,data,fig):
        S=data # generate data
        lowestPoint=get_lowest_point(S) #　 search lowest points
        pointOnHull=lowestPoint  #  lowest and leftmost point  in S 
        n=len(S) #S total count
        i=0 
        path = [None]*n   

        # animation plot
        epoch=0
        
        a = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().pack()
        
        while True:
            path[i]=pointOnHull
            endPoint=S[0]
            for j in range(1,n):
                if (endPoint[0] == pointOnHull[0] and endPoint[1] == pointOnHull[1]) or not CCW(S[j],path[i],endPoint):
                    endPoint = S[j]
            i=i+1
            pointOnHull = endPoint

            tmpPath=np.array([path[k] for k in range(n) if path[k] is not None])
            print(tmpPath)
            if len(tmpPath) > 1 :
                #plt.clf()
                a.plot(tmpPath[:,0],tmpPath[:,1],'b-',picker=5)
                a.plot(S[:,0],S[:,1],".r")
                a.axis('on')
                a.set_xlabel('epoch {0}'.format(epoch))
                #plt.show(block=false)
                #plt.pause(0.0000001)
                canvas.draw()
                epoch+=1
            else:pass


            if endPoint[0] == path[0][0] and endPoint[1] == path[0][1]:
                break
        
        path=clear_path(path)
        #return path,S

def generate_data(low,high,size):
    return np.random.randint(low,high,size=size)
def CCW(a,b,c):
    if (b[0]-a[0])*(c[1]-a[1]) >= (c[0]-a[0])*(b[1]-a[1]) :
        return True
    return False
def clear_path(p):
    while p[-1] is None :
        p.pop(-1)
    p=np.array(p)
    return p
def get_lowest_point(data):
    lowsetPoint=np.zeros((1,2))
    for index,item in enumerate(data):
        if index == 0:
            lowsetPoint=item
        elif lowsetPoint[1]>=item[1] or (lowsetPoint[1]==item[1] and lowsetPoint[0]<item[0]):
            lowsetPoint=item
    return lowsetPoint

window=tk.Tk()
start=GUI(window)
start.print_selection()
start.add_radiobtn()
window.mainloop()