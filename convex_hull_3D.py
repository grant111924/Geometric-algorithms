from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import itertools
from tqdm import tqdm
def generate_data(n,size):
    return np.random.randint(n,size=size)

def plot(set_P,un_set_point):
    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    xs=set_P[:,0]
    ys=set_P[:,1] 
    zs=set_P[:,2]
    ax.scatter(xs,ys,zs,c='b',marker='o')
    #xv=set_P[:4,:]
    set_facet=[]
    for planar in itertools.combinations(un_set_point,3):
        set_facet.append(list(planar))
    print(len(un_set_point))
    for index ,face in enumerate(set_facet):
        xv=face
        ax.plot ( [ xv[0][0], xv[1][0] ], [ xv[0][1], xv[1][1] ], [ xv[0][2],xv[1][2] ], 'r' )
        ax.plot ( [ xv[0][0], xv[2][0] ], [ xv[0][1], xv[2][1] ], [ xv[0][2], xv[2][2] ], 'r' )
        #ax.plot ( [ xv[0,0], xv[3,0] ], [ xv[0,1], xv[3,1] ], [ xv[0,2], xv[3,2] ], 'r' )
        ax.plot ( [ xv[1][0], xv[2][0] ], [ xv[1][1], xv[2][1] ], [ xv[1][2], xv[2][2] ], 'r' )
        #ax.plot ( [ xv[1,0], xv[3,0] ], [ xv[1,1], xv[3,1] ], [ xv[1,2], xv[3,2] ], 'r' )
        #ax.plot ( [ xv[2,0], xv[3,0] ], [ xv[2,1], xv[3,1] ], [ xv[2,2], xv[3,2] ], 'r' )

    plt.show()

def find_tetrahedron(set_P) :
    while True:
        
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

def find_tetrahedron_new(set_P):
    while True:
        vectorAB=set_P[0]-set_P[1]
        vectorAC=set_P[0]-set_P[2]
        if np.sum(np.cross(vectorAB,vectorAC))!=0:
            face=[set_P[0],set_P[1],set_P[2]]
            fourCentroid=first_centroid(set_P,face)
            faceIndex=[0,1,2]

            face1=[set_P[3],set_P[0],set_P[1]]
            a,b,c,d=compute_plane(face1)
            if is_Visible(a,b,c,d,fourCentroid): 
                face1=filp(face1)
                face1Index=[0,3,1]
            else:face1Index=[3,0,1]
                
            face2=[set_P[3],set_P[1],set_P[2]]
            a,b,c,d=compute_plane(face2)
            if is_Visible(a,b,c,d,fourCentroid): 
                face2=filp(face2)
                face2Index=[1,3,2]
            else:face2Index=[3,1,2]

            face3=[set_P[3],set_P[2],set_P[0]]
            a,b,c,d=compute_plane(face3)
            if is_Visible(a,b,c,d,fourCentroid): 
                face3=filp(face3)
                face3Index=[2,3,0]
            else:face3Index=[3,2,0]
            
            faceList=[face,face1,face2,face3]
            faceIndexList=[faceIndex,face1Index,face2Index,face3Index]
            break
        else:
            np.random.shuffle(set_P)

    return faceList,faceIndexList,set_P       
  
def first_centroid(set_P,face):
    x=(set_P[0][0]+set_P[1][0]+set_P[2][0]+set_P[3][0])/4
    y=(set_P[0][1]+set_P[1][1]+set_P[2][1]+set_P[3][1])/4
    z=(set_P[0][2]+set_P[1][2]+set_P[2][2]+set_P[3][2])/4
    centroid=np.array([x,y,z])
    return centroid

def filp(face):
    tmp=face[0]
    face[0]=face[1]
    face[1]=tmp
    return face

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
def conflict_graph(set_Remain,tetrahedron):
    set_facet=tetrahedron
    conflictListP=[]
    conflictListF=[]
    for pointIndex, point in enumerate(set_P):
        if pointIndex >3 : 
            facePairList=[]
            for faceIndex, face in enumerate(set_facet):
                a,b,c,d=compute_plane(face)
                if is_Visible(a,b,c,d,point):
                    facePairList.append(faceIndex)
            conflictListP.append(facePairList)
        else :
            conflictListP.append([])
    for faceIndex, face in enumerate(set_facet):
        pointPairList=[]
        a,b,c,d=compute_plane(face)
        for pointIndex, point in enumerate(set_P):
            if pointIndex > 3:
                if is_Visible(a,b,c,d,point):
                    pointPairList.append(pointIndex)
        conflictListF.append(pointPairList)

    return conflictListP,conflictListF

def main(set_P,firstTetrahedron,firstIndexList):
    set_facet=[]
    set_facet_toPointIndexList=firstIndexList
    for faceIndex,face in enumerate(firstTetrahedron):
        set_facet.append(face)
    #print(set_facet)
    #init conflict graph
    conflictP_findF,conflictF_findP=conflict_graph(set_P,firstTetrahedron)
    print("conflictP_findF:",conflictP_findF)
    print("conflictF_findP:",conflictF_findP)
    
    for pointIndex,point in enumerate(set_P):
        if pointIndex >3 and len(conflictP_findF[pointIndex])!=0:
            insidePointList=list(range(0, pointIndex))  #[0 ~ potintIndex-1]
            print(insidePointList)
            print("pointIndex:%d list: %s"%(pointIndex,conflictP_findF[pointIndex]))
            #Delete all facets in conflictP_findF[pointIndex] from graph 
            #create the boundary of visible region of pointIndex and create horizon edges in order  (counterclockwise)
            
            visibleList=conflictP_findF[pointIndex]
            visiblePointListTmp,visiblePointList,boundaryPointList,edgePairList=[],[],[],[]
            
            for i in range(len(visibleList)): #this point can see the points of the facets merge in list 
                visiblePointListTmp+=set_facet_toPointIndexList[visibleList[i]]   
            visiblePointList=list(set(visiblePointListTmp))
            
            for i  in range(len(visiblePointList)):
                if visiblePointList[i] in insidePointList :#Intersection between visible point set and unvisible point set is boundary
                    boundaryPointList.append(visiblePointList[i])     
                               
            
            
            
            print("visiblePointList:",visiblePointList)
            print("boundaryPointList:",boundaryPointList)
            print("=============================")
            #visibleFaceList,unVisibleFaceList=get_facet_point(set_facet,visibleList)
            #visibleEdgeList=get_boundary_point(visibleFaceList,unVisibleFaceList)

            
def get_facet_point(set_facet,visibleList):
    unVisibleFaceList=[]
    visibleFaceList=[]
    for i in range(len(set_facet)):
        if i not in visibleList:
            unVisibleFaceList.append(set_facet[i])
        else :  
            visibleFaceList.append(set_facet[i])  
    return visibleFaceList,unVisibleFaceList

def get_boundary_point(visibleFaceList,unVisibleFaceList):
    edgeSet=[]
    visiblePointList=[]
    unVisiblePointList=[]
    for faceIndex,face in enumerate(visibleFaceList):
        for pointIndex,point in enumerate(face):
            visiblePointList.append(point)

    for faceIndex,face in enumerate(unVisibleFaceList):
        for pointIndex,point in enumerate(face):
            unVisiblePointList.append(point)

    
    return edgeSet          
            


       

if __name__ == "__main__":
    set_P_count=20
    set_P=generate_data(10,(set_P_count,3))
    firstTetrahedron,firstIndexList,set_P=find_tetrahedron_new(set_P)
    #plot(set_P,firstTetrahedron)
 
    #set_Remain=np.delete(set_P,[0,1,2,3],axis=0)
    main(set_P,firstTetrahedron,firstIndexList)
    """set_facet=main(set_Remain,firstTetrahedron)
    print(set_facet)
    set_point=[]
    for i in range(len(set_facet)):
        for j in range(len(set_facet[i])):
            set_point.append(list(set_facet[i][j]))

    print(set_point)
    un_set_point=[]
    for i , p in enumerate(set_point):
        if i==0:un_set_point.append(p)
        else: 
            if p not in un_set_point:
                un_set_point.append(p)
    print(un_set_point)
    plot(set_P,un_set_point)
    """