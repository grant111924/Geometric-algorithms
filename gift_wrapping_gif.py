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
    S=generate_data(0,20,size=(50,2)) # generate data
    lowestPoint=get_lowest_point(S) #　 search lowest points
    pointOnHull=lowestPoint  #  lowest and leftmost point  in S 
    n=len(S) #S total count
    i=0 
    path = [None]*n   

    # animation plot
    epoch=0
    plt.figure()

    while True:
        path[i]=pointOnHull
        endPoint=S[0]
        for j in range(1,n):
            if (endPoint[0] == pointOnHull[0] and endPoint[1] == pointOnHull[1]) or not CCW(S[j],path[i],endPoint):
                endPoint = S[j]
        i=i+1
        pointOnHull = endPoint

        tmpPath=np.array([path[k] for k in range(n) if path[k] is not None])
       
        if len(tmpPath) > 1 :
            plt.clf()
            plt.plot(tmpPath[:,0],tmpPath[:,1],'b-',picker=5)
            plt.plot(S[:,0],S[:,1],".r")
            plt.axis('on')
            plt.xlabel('epoch {0}'.format(epoch))
            plt.show(block=False)
            plt.pause(0.01)
            epoch+=1
        
        if endPoint[0] == path[0][0] and endPoint[1] == path[0][1]:
            break
    
    path=clear_path(path)
#    return path,S
    plt.close()
    final_plot(path,S,plt)

def clear_path(p):
    while p[-1] is None :
        p.pop(-1)
    p=np.array(p)
    return p


def final_plot(L,P,plt):  
    plt.clf()
    #plt.figure()
    plt.plot(L[:,0],L[:,1], 'b-', picker=5)
    plt.plot([L[-1,0],L[0,0]],[L[-1,1],L[0,1]], 'b-', picker=5)
    plt.plot(P[:,0],P[:,1],".r")
    plt.xlabel('Final result')
    plt.axis('on')
    plt.show()


if __name__ == "__main__":
    #path,total=gift_wrapping()
    gift_wrapping()