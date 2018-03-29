import numpy as np 
import matplotlib.pyplot as plt 
import math, random
from scipy.linalg import solve
def generate_data(low,high,size):
    return np.random.randint(low,high,size=size)

def min_circle(P):
    c=None
    P=np.random.permutation(P)
    if c is None :
        print("Create circle")
        c=make_circle(P[0],P[1])
    for index,item in enumerate(P):
        if is_in_circle(c,item):
            print("第一層 ：圈內，第%d個" %(index))
        else :
            print("p_i is not in circle")
            c=min_circle_with_point(P[:index+1],item)
            print(c)
    return c
def min_circle_with_point(S,p):
    c=make_circle(S[0],p)
    for index,item in enumerate(S):
        if is_in_circle(c,item):
            print("第二層： total:%d 圈內，第%d個" %(len(S),index))
        else:
            print("p_j is not in circle")    
            c = min_circle_with_two_point(S[:index+1], p, item)
    return c 
def min_circle_with_two_point(T,P,p):
    c=make_circle(P,p)
    left = None
    right = None
    for index, item in enumerate(T):
        if is_in_circle(c,item):
            print("第三層： total:%d 圈內，第%d個" %(len(T),index))
        else:
            print("p_k is not in circle") 
            c=make_circumcircle(item,P,p)
            cross = _cross_product(P[0],P[1],p[0],p[1], item[0], item[1])
            if c is None:
                continue
            elif cross > 0.0 and (left is None or _cross_product(P[0],P[1],p[0],p[1], c[0], c[1]) > _cross_product(P[0],P[1],p[0],p[1], left[0], left[1])):
                left = c
            elif cross < 0.0 and (right is None or _cross_product(P[0],P[1],p[0],p[1], c[0], c[1]) < _cross_product(P[0],P[1],p[0],p[1], right[0], right[1])):
                right = c  

    # Select which circle to return
    if left is None and right is None:
        return c
    elif left is None:
        return right
    elif right is None:
        return left
    else:
        return left if (left[2] <= right[2]) else right
    
    
    return c


def is_in_circle(c,p):
    if c is not None and pow((p[0]-c[0]),2)+pow((p[1]-c[1]),2) <=pow(c[2],2):return True
    else: return False


def plot(c,P):
    fig = plt.figure()
    ax = fig.add_subplot(111) 
    circle1 =plt.Circle((c[0],c[1]),radius=c[2])
    plt.plot(c[0],c[1],".g")
    plt.plot(P[:,0],P[:,1],".r")
    plt.xlim(-10,30)
    plt.ylim(-10,30)
    ax.add_patch(circle1) 
    plt.show()
    
def make_circle(a,b):
    c=np.zeros((3,)) # [x,y,r]
    c[0]=(a[0]+b[0])/2
    c[1]=(a[1]+b[1])/2
    c[2]=math.sqrt(pow((a[0]-b[0]),2)+pow((a[1]-b[1]),2))/2
    return c

def make_circumcircle(p0,p1,p2):
    ax, ay = p0
    bx, by = p1
    cx, cy = p2
    ox = (min(ax, bx, cx) + max(ax, bx, cx)) / 2.0
    oy = (min(ay, by, cy) + max(ay, by, cy)) / 2.0
    ax -= ox; ay -= oy
    bx -= ox; by -= oy
    cx -= ox; cy -= oy
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
    if d == 0.0:
        return None
    x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    ra = math.hypot(x - p0[0], y - p0[1])
    rb = math.hypot(x - p1[0], y - p1[1])
    rc = math.hypot(x - p2[0], y - p2[1])
    c=np.zeros((3,))
    c[0]=x
    c[1]=y
    c[2]= max(ra, rb, rc)
    return c

def _cross_product(x0, y0, x1, y1, x2, y2):
	return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)

if __name__ == "__main__":
    data=generate_data(0,20,size=(20,2))
    circle=min_circle(data)
    plot(circle,data)
    

