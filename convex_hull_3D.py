from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import itertools
from tqdm import tqdm

def generate_data(n,size):
    return np.random.randint(n,size=size)

def tetrahedron_plot(set_P,set_facet):
    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    xs=set_P[:,0]
    ys=set_P[:,1] 
    zs=set_P[:,2]
    ax.scatter(xs,ys,zs,c='b',marker='o')
    for index ,face in enumerate(set_facet):
        xv=[set_P[face[0]],set_P[face[1]],set_P[face[2]]]
        #xv=face
        ax.plot ( [ xv[0][0], xv[1][0] ], [ xv[0][1], xv[1][1] ], [ xv[0][2],xv[1][2] ], 'r' )
        ax.plot ( [ xv[0][0], xv[2][0] ], [ xv[0][1], xv[2][1] ], [ xv[0][2], xv[2][2] ], 'r' )
        #ax.plot ( [ xv[0,0], xv[3,0] ], [ xv[0,1], xv[3,1] ], [ xv[0,2], xv[3,2] ], 'r' )
        ax.plot ( [ xv[1][0], xv[2][0] ], [ xv[1][1], xv[2][1] ], [ xv[1][2], xv[2][2] ], 'r' )
        #ax.plot ( [ xv[1,0], xv[3,0] ], [ xv[1,1], xv[3,1] ], [ xv[1,2], xv[3,2] ], 'r' )
        #ax.plot ( [ xv[2,0], xv[3,0] ], [ xv[2,1], xv[3,1] ], [ xv[2,2], xv[3,2] ], 'r' )
    plt.show()
  

def find_tetrahedron(set_P):
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

def get_centroid(set_P,face):
    p1=set_P[face[0]]
    p2=set_P[face[1]]
    p3=set_P[face[2]]
    centroidPointX=(p1[0]+p2[0]+p3[0])/3
    centroidPointY=(p1[1]+p2[1]+p3[1])/3
    centroidPointZ=(p1[2]+p2[2]+p3[2])/3
    return np.array([centroidPointX,centroidPointY,centroidPointZ])

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
def is_Coplanar(plane1,plane2):
    plane1=np.array(plane1)
    plane2=np.array(plane2)
    return np.all(plane1 * np.linalg.norm(plane2) - plane2 * np.linalg.norm(plane1) == 0)

def conflict_graph(num,set_Remain,tetrahedron):
    set_facet=tetrahedron
    conflictListP=[]
    conflictListF=[]
    for pointIndex, point in enumerate(set_P):
        if pointIndex > num : 
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
            if pointIndex > num:
                if is_Visible(a,b,c,d,point):
                    pointPairList.append(pointIndex)
        conflictListF.append(pointPairList)

    return conflictListP,conflictListF

def counterclockwise(p,bList,set_P):
    totalPointSum=np.array([0,0,0])
    sortIndexList,sortList=[],[]
    for i in range(len(bList)):
        index=bList[i]
        if i == 0 : 
            totalPointSum+=set_P[index]    
        else:    
            totalPointSum+=set_P[index]
    center=totalPointSum/len(bList)
    print(center)
    for index, pointIndex in enumerate(bList):
        if index== 0:
            tmp=set_P[pointIndex]
            sortList.append((0,pointIndex))
        else: 
            x=np.dot(center-p,np.cross(tmp-center,set_P[pointIndex]-center))
            sortList.append((x,pointIndex))
    sortIndexList=sorted(sortList,key=lambda s: s[0])
    result=[]
    for index,item in enumerate(sortIndexList):
        result.append(item[1])
    return result
    
def main(set_P,firstTetrahedron,firstIndexList):
    set_facet=[]
    set_facet_toPointIndexList=firstIndexList
    for faceIndex,face in enumerate(firstTetrahedron):
        set_facet.append(face)
    #init conflict graph
    conflictP_findF,conflictF_findP=conflict_graph(3,set_P,firstTetrahedron)
    print("conflictP_findF:",conflictP_findF)
    print("conflictF_findP:",conflictF_findP)
    
    for pointIndex,point in enumerate(set_P):
        if pointIndex >3 and len(conflictP_findF[pointIndex])!=0:
            insidePointList=list(range(0, pointIndex))  #[0 ~ potintIndex-1]
            print(insidePointList)
            print("pointIndex:%d list: %s"%(pointIndex,conflictP_findF[pointIndex]))
            #Delete all facets in conflictP_findF[pointIndex] from graph 
            visibleList=conflictP_findF[pointIndex]
            #print("visibleList:",visibleList)
            #print("set_facet_toPointIndexList:",set_facet_toPointIndexList)

            set_facet_toPointIndexList_afterDel=[]
            for index,item in enumerate(set_facet_toPointIndexList):
                if index not in visibleList:
                    set_facet_toPointIndexList_afterDel.append(item)
            #print("set_facet_toPointIndexList_afterDel:",set_facet_toPointIndexList_afterDel)
            #tetrahedron_plot(set_P,set_facet_toPointIndexList_afterDel)
            #create the boundary of visible region of pointIndex and create horizon edges in order  (counterclockwise)
            visiblePointListTmp,visiblePointList,boundaryPointList,edgePairList=[],[],[],[]

            #this point can see the points of the facets merge in list 
            for i in range(len(visibleList)): 
                visiblePointListTmp+=set_facet_toPointIndexList[visibleList[i]]   
            visiblePointList=list(set(visiblePointListTmp))

            #Intersection between visible point set and unvisible point set is boundary
            for i  in range(len(visiblePointList)):
                if visiblePointList[i] in insidePointList :
                    boundaryPointList.append(visiblePointList[i])   

            # counterclockwise order boundary point set and create edge list                   
            edgePointList=counterclockwise(point,boundaryPointList,set_P)
            for i in range(len(edgePointList)):
                if (i+1) < len(edgePointList):
                    edgePairList.append([edgePointList[i],edgePointList[i+1]])
                else :
                    edgePairList.append([edgePointList[-1],edgePointList[0]])
            

            print("edgePairList:",edgePairList)
            set_facet_toPointIndexList_add=[]
            for eIndex, edge in enumerate(edgePairList):#先找是否共邊 再判斷共面
                newFacet=[edge[0],edge[1],pointIndex]
                set_facet_toPointIndexList_add.append(newFacet)
            #tetrahedron_plot(set_P,set_facet_toPointIndexList_add)
            """for  i ,fIndex in enumerate(set_facet_toPointIndexList):
                if edge[0] in fIndex and edge[1] in fIndex:
                    newFacetPoint=[]
                    for i in range(len(newFacet)):
                        newFacetPoint.append(set_P[newFacet[i]])
                    if is_Coplanar(compute_plane(newFacetPoint),compute_plane(set_facet[i])):
                        newFacet+=set_facet
                        newFacet=list(set(newFacet))
                        facet_toPointIndexList.append(newFacet)
                else:
                    facet_toPointIndexList.append(newFacet)"""
                    
                            
            #set_facet_toPointIndexList_add+=facet_toPointIndexList       
            set_facet_toPointIndexList_add+= set_facet_toPointIndexList_afterDel
            set_facet_toPointIndexList=set_facet_toPointIndexList_add
            print("set_facet_toPointIndexList_add :",set_facet_toPointIndexList_add)
            set_facet_toPointIndexList_finalDel=[]
            for fIndex, face in enumerate(set_facet_toPointIndexList):
                center=get_centroid(set_P,face)
                for i, f in enumerate(set_facet_toPointIndexList):
                    if i!=fIndex:
                        fPoint=[]
                        for j in range(len(f)):
                            fPoint.append(set_P[f[j]])
                        a,b,c,d=compute_plane(fPoint)
                        if is_Visible(a,b,c,d,center):
                             set_facet_toPointIndexList_finalDel.append(f)
            #set_facet_toPointIndexList_finalDel=list(set(set_facet_toPointIndexList_finalDel))
            print("set_facet_toPointIndexList_finalDel",set_facet_toPointIndexList_finalDel)
            print("set_facet_toPointIndexList_add",set_facet_toPointIndexList_add)



            #update conflict graph
            newConvexHull=[]
            for fIndex,face in enumerate(set_facet_toPointIndexList_add):
                p1=set_P[face[0]]
                p2=set_P[face[1]]
                p3=set_P[face[2]]
                newConvexHull.append([p1,p2,p3])
            conflictP_findF,conflictF_findP=conflict_graph(pointIndex,set_P,newConvexHull)
            print("set_facet_toPointIndexList :",set_facet_toPointIndexList)
            print("conflictP_findF new:",conflictP_findF)
            print("conflictF_findP new:",conflictF_findP)

    tetrahedron_plot(set_P,set_facet_toPointIndexList)

        

        

       

if __name__ == "__main__":
    set_P_count=10
    set_P=generate_data(10,(set_P_count,3))
    firstTetrahedron,firstIndexList,set_P=find_tetrahedron(set_P)
    tetrahedron_plot(set_P,firstIndexList)
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