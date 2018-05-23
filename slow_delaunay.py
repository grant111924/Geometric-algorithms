import numpy as np
import matplotlib.pyplot as plt
import math
def generate_data(low,high,size):
    return np.random.randint(low,high,size=size)

def super_triangle(data):
    p0=np.zeros((1,2))
    for index,coordinate in enumerate(data):
        if index == 0 :
            p0=coordinate
        else :    
            p0=np.maximum(coordinate,p0)



if __name__ =="__main__":
    data=generate_data(0,20,size=(10,2))
    super_triangle(data)