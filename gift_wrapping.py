#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
"""
class gift_wrapping():
    def __init__(self):
        pass
"""

def generate_data(low,high,size):
    return np.random.randint(low,high,size=size)
def get_loweset_point(data):
    lowsetPoint=np.zeros((1,2))
    for index,item in enumerate(data):
        if index == 0:
            lowsetPoint=item
        elif lowsetPoint[1]>=item[1] or (lowsetPoint[1]==item[1] and lowsetPoint[0]<item[0]):
            lowsetPoint=item
    return lowsetPoint
def select_point():
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
    data=generate_data(0,20,size=(10,2))
    print(data)
    x=get_loweset_point(data)
    print(x)
    plot(data)

    pass