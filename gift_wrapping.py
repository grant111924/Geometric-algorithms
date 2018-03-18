#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def generate_data(low,high,size):
    return np.random.randint(low,high,size=size)
def get_lowest_point(data):
    lowsetPoint=np.zeros((1,2))
    start=0
    for index,item in enumerate(data):
        if index == 0:
            lowsetPoint=item
        elif lowsetPoint[1]>=item[1] or (lowsetPoint[1]==item[1] and lowsetPoint[0]<item[0]):
            lowsetPoint=item
            start=index
    return lowsetPoint,start
def CCW(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])
def main():
    data=generate_data(0,20,size=(10,2))
    lowestPoint,start=get_lowest_point(data)
    
    n=len(data)
    endPoint=lowestPoint
    path=[]
    path.append(start)# first point
    for i in range(1,n):
	    if (endPoint[0] == pointOnHull[0] and endpoint[1] == pointOnHull[1]) or not CCW(data[i],P[i],endPoint):
			endPoint = data[i]


    pass

def plot(data):
    x=[]
    y=[]
    for item  in data:
        x.append(item[0])
        y.append(item[1])
    print(x)
    print(y)
    plt.plot(x,y,'ro')
    plt.axis([0, 20, 0, 20])
    plt.show()

if __name__ == "__main__":
    
    main()
    #plot(data)
    