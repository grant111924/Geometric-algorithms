#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def generate_data(low,high,size):
    return np.random.randint(low,high,size=size)
def get_lowest_point(data):
    lowsetPoint=np.zeros((1,2))
    for index,item in enumerate(data):
        if index == 0:
            lowsetPoint=item
        elif lowsetPoint[1]>=item[1] or (lowsetPoint[1]==item[1] and lowsetPoint[0]<item[0]):
            lowsetPoint=item
    return lowsetPoint

def CCW(a,b,c):
    if (b[0]-a[0])*(c[1]-a[1]) >= (c[0]-a[0])*(b[1]-a[1]) :
        return True
    return False

def gift_wrapping():
    S=generate_data(0,20,size=(10,2))
    lowestPoint=get_lowest_point(S) #　 search lowest points
    pointOnHull=lowestPoint  #  lowest and leftmost point  in S 
    n=len(S) #S total count
    i=0 
    print(S)
    path = [None]*n   
    while True:
        #print(path[i])
        path[i]=pointOnHull
        endPoint=S[0]
        for j in range(1,n):
            if (endPoint[0] == pointOnHull[0] and endPoint[1] == pointOnHull[1]) or not CCW(S[j],path[i],endPoint):
                endPoint = S[j]
        i=i+1
        pointOnHull = endPoint
        if endPoint[0] == path[0][0] and endPoint[1] == path[0][1]:
            break
     

    while path[-1] is None :
        path.pop(i)
    print(path) 
    path=np.array(path)
    return path,S
def plot(L,P):

    plt.figure()
    plt.plot(L[:,0],L[:,1], 'b-', picker=5)
    plt.plot([L[-1,0],L[0,0]],[L[-1,1],L[0,1]], 'b-', picker=5)
    plt.plot(P[:,0],P[:,1],".r")
    plt.axis('off')
    plt.show()
    
if __name__ == "__main__":
    
    data,total=gift_wrapping()
    plot(data,total)
    