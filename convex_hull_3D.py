from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
from tqdm import tqdm
def generate_data(n,size):
    return np.random.randint(n,size=size)

def plot(set_P,set_facet):
    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    xs=set_P[:,0]
    ys=set_P[:,1] 
    zs=set_P[:,2]
    ax.scatter(xs,ys,zs,c='b',marker='o')
    #xv=set_P[:4,:]
    for index ,face in enumerate(set_facet):
        xv=face
        ax.plot ( [ xv[0,0], xv[1,0] ], [ xv[0,1], xv[1,1] ], [ xv[0,2], xv[1,2] ], 'r' )
        ax.plot ( [ xv[0,0], xv[2,0] ], [ xv[0,1], xv[2,1] ], [ xv[0,2], xv[2,2] ], 'r' )
        #ax.plot ( [ xv[0,0], xv[3,0] ], [ xv[0,1], xv[3,1] ], [ xv[0,2], xv[3,2] ], 'r' )
        ax.plot ( [ xv[1,0], xv[2,0] ], [ xv[1,1], xv[2,1] ], [ xv[1,2], xv[2,2] ], 'r' )
        #ax.plot ( [ xv[1,0], xv[3,0] ], [ xv[1,1], xv[3,1] ], [ xv[1,2], xv[3,2] ], 'r' )
        #ax.plot ( [ xv[2,0], xv[3,0] ], [ xv[2,1], xv[3,1] ], [ xv[2,2], xv[3,2] ], 'r' )

    plt.show()

def find_tetrahedron(set_P) :
    while True:
        np.random.shuffle(set_P)
        p1=set_P[0]
        p2=set_P[1]
        p3=set_P[2]
        p4=set_P[3]
        p1p2=p2-p1
        p1p3=p3-p1
        print(np.cross(p1p2,p1p3))
        if  np.count_nonzero(np.cross(p1p2,p1p3)) ==3 :
            p1p4=p4-p1
            print(np.dot(p1p4,np.cross(p1p2,p1p3)))
            if np.dot(p1p4,np.cross(p1p2,p1p3)) !=0: break # AD。(AB X AC) = 0 => coplanar
        else : continue
    return p1,p2,p3,p4,set_P            

def compute_plane(face): #用平面方程式：ax+by+cz+d=0  ==>  大於0就是看得到
    a  =  (face[1][1]-face[0][1])*(face[2][2]-face[0][2])-(face[1][2]-face[0][2])*(face[2][1]-face[0][1])
    b  =  (face[1][2]-face[0][2])*(face[2][0]-face[0][0])-(face[1][0]-face[0][0])*(face[2][2]-face[0][2])
    c  =  (face[1][0]-face[0][0])*(face[2][1]-face[0][1])-(face[1][1]-face[0][1])*(face[2][0]-face[0][0])
    d  =  0-(a*face[0][0]+b*face[0][1]+c*face[0][2])  
    return a,b,c,d

def is_Visible(a,b,c,d,point):
    return (a*point[0]+b*point[1]+c*point[2]+d)>0

def get_centroid(face):
    p1=face[0]
    p2=face[1]
    p3=face[2]
    centroidPointX=(p1[0]+p2[0]+p3[0])/3
    centroidPointY=(p1[1]+p2[1]+p3[1])/3
    centroidPointZ=(p1[2]+p2[2]+p3[2])/3
    return np.array([centroidPointX,centroidPointY,centroidPointZ])

def main(set_Remain,set_C):
    #兩種狀態 visible invisible
    """convexEdge_count=6
    convexPoint_count=4
    convexFacet_count=2+convexEdge_count-convexPoint_count"""
    set_facet=[]    
    #point_conflict=[]
    #facet_conflict=[]
    for planar in itertools.combinations(set_C,3):
        set_facet.append(list(planar))
    
    tmpFaceSet=[]
    visibleFacetList=[] 

    for pointIndex, point in tqdm(enumerate(set_Remain)): #還沒加入的點集
        
        tmp_set_facet=[] #原本的facet 資訊給 tmp 做完處理後並更新 
        for faceIndex,face in enumerate(set_facet):
            tmp_set_facet.append(face)
        #挑出該點 看得到的facet  
        for faceIndex,face in enumerate(set_facet):  
            a,b,c,d=compute_plane(face)# 算出平面方程式 
            if is_Visible(a,b,c,d,point): 
                visibleFacetList.append(faceIndex)
        #print("Index: %d visible Face List %s " %(pointIndex,visibleFacetList))
        
        if  len(visibleFacetList) == 0 : continue # 表示在Convex Hull 內
        
        # 將該點看得到的面 從 tmp_set_face (被認定為convex hull的部分) 剔除
        for index ,faceIndex  in enumerate(visibleFacetList):
            #if tmp_set_facet[faceIndex] in set_facet : set_facet.remove(tmp_set_facet[faceIndex])
            face=tmp_set_facet[faceIndex]
            try:
                index=set_facet.index(face)
            except ValueError :
                continue 
            else:
                set_facet.pop(index)
        # 如果剛好只看到一個facet     
        if  len(visibleFacetList) == 1 : # 直接 與 該facet三個點 連接 並消除 該facet
            faceIndex=visibleFacetList[0]
            oldPlanar=tmp_set_facet[faceIndex]
            set_facet.append(np.array([point,oldPlanar[0],oldPlanar[1]]))
            set_facet.append(np.array([point,oldPlanar[1],oldPlanar[2]]))
            set_facet.append(np.array([point,oldPlanar[0],oldPlanar[2]]))
            continue 
        else : # 可以看到很多個facet
            
            for index ,faceIndex  in enumerate(visibleFacetList):
                oldPlanar=tmp_set_facet[faceIndex]
                tmpFaceSet.append(np.array([point,oldPlanar[0],oldPlanar[1]]))
                tmpFaceSet.append(np.array([point,oldPlanar[1],oldPlanar[2]]))
                tmpFaceSet.append(np.array([point,oldPlanar[0],oldPlanar[2]]))
            
            for faceIndex, face in  enumerate(tmpFaceSet):
                for otherIndex, otherFace in enumerate(tmpFaceSet):
                    if faceIndex != otherIndex :
                        a,b,c,d=compute_plane(face)
                        if is_Visible(a,b,c,d,get_centroid(otherFace)):
                            face=None
                            break
                if face is not None:
                    set_facet.append(face)
    
    #fig=plt.figure()
    #ax=fig.add_subplot(111,projection='3d')
    return set_facet
        
       

if __name__ == "__main__":
    set_P_count=15
    set_P=generate_data(30,(set_P_count,3))
    p1,p2,p3,p4,set_P=find_tetrahedron(set_P)
    set_C=np.array(set_P[:4])
    set_Remain=np.delete(set_P,[0,1,2,3],axis=0)
    set_facet=main(set_Remain,set_C)
    plot(set_P,set_facet)
"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()"""