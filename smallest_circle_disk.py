import numpy as np 
import matplotlib.pyplot as plt 
import math, random
def generate_data(low,high,size):
    return np.random.randint(low,high,size=size)

def min_circle(P):
    c=None
    S=[]
    if c is None: # 一開始先給兩點作為圓
        c=make_circle(P[0],P[1])
        S.append(P[0])
        S.append(P[1])
    for i,item in enumerate(P[2:]):
        if is_in_circle(c,item):
            S=list(S)
            S.append(item)
        else:
            S=np.array(S)
            S=np.random.permutation(S)
            c=min_circle_with_point(S,item)

    return c
def min_circle_with_point(S,p):
    print(S)
    c_1=make_circle(S[0],p)
    print(c_1)
    T=[]
    T.append(S[0])
    for i,item in enumerate(S[1:]):
        if is_in_circle(c_1,item):
            c_1=min_circle_with_two_point(T,S[0],item)
        else:
            T.append(item)
    return c_1


def min_circle_with_two_point(T,P,p):
    print(T)
    print(p)
    print(P)
    c_0=make_circle(P,p)
    left = None
    right = None
    for i,item in enumerate(T):
        if  is_in_circle(c_0,item):
            continue
        cross = _cross_product(P[0], P[1], p[0], p[1], item[0], item[1])
        c=make_circumcircle(P,p,item)
        if c is None:
            continue
        elif cross > 0.0 and (left is None or _cross_product(P[0], P[1], p[0], p[1], c[0], c[1]) > _cross_product(P[0], P[1], p[0], p[1], left[0], left[1])):
            left = c
        elif cross < 0.0 and (right is None or _cross_product(P[0], P[1], p[0], p[1], c[0], c[1]) < _cross_product(P[0], P[1], p[0], p[1], right[0], right[1])):
            right = c

    # Select which circle to return
    if left is None and right is None:
        return c_0
    elif left is None:
        return right
    elif right is None:
        return left
    else:
        return left if (left[2] <= right[2]) else right




def is_in_circle(c,p):
    if pow((p[0]-c[0]),2)+pow((p[1]-c[1]),2) <=pow(c[2],2):return True
    else: return False


def plot(c,P):
    fig = plt.figure()
    ax = fig.add_subplot(111) 
    circle1 =plt.Circle((c[0],c[1]),radius=c[2])
    plt.plot(P[:,0],P[:,1],".r")
    plt.xlim(0,20)
    plt.ylim(0,20)
    ax.add_patch(circle1) 
    plt.show()
    
def make_circle(a,b):
    c=np.zeros((3,)) # [x,y,r]
    c[0]=(a[0]+b[0])/2
    c[1]=(a[1]+b[1])/2
    c[2]=math.sqrt(pow((a[0]-b[0]),2)+pow((a[1]-b[1]),2))/2
    return c

def make_circumcircle(p0, p1, p2):
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
    return (x, y, max(ra, rb, rc))

def _cross_product(x0, y0, x1, y1, x2, y2):
	return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)

if __name__ == "__main__":
    data=generate_data(0,20,size=(20,2))
    circle=min_circle(data)
    plot(circle,data)
    

