def main_old(set_Remain,firstTetrahedron):
    #兩種狀態 visible invisible
    #conflict_graph(set_Remain,firstTetrahedron)
    set_facet=firstTetrahedron    
    #point_conflict=[]
    #facet_conflict=[]

    """for planar in itertools.combinations(set_C,3):
        set_facet.append(list(planar))"""

    for pointIndex, point in tqdm(enumerate(set_Remain)): #還沒加入的點集
        visibleFacetList=[] 
        tmp_set_facet=[] #原本的facet 資訊給 tmp 做完處理後並更新 
        for faceIndex,face in enumerate(set_facet):
            tmp_set_facet.append(face)
        #挑出該點 看得到的facet  
        for faceIndex,face in enumerate(set_facet):  
            a,b,c,d=compute_plane(face)# 算出平面方程式 
            if is_Visible(a,b,c,d,point): 
                visibleFacetList.append(faceIndex)
        print("Index: %d visible Face List %s " %(pointIndex,visibleFacetList))
        
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
            tmpFaceSet=[]
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

    return set_facet

def get_centroid(face):
    p1=face[0]
    p2=face[1]
    p3=face[2]
    centroidPointX=(p1[0]+p2[0]+p3[0])/3
    centroidPointY=(p1[1]+p2[1]+p3[1])/3
    centroidPointZ=(p1[2]+p2[2]+p3[2])/3
    return np.array([centroidPointX,centroidPointY,centroidPointZ])


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


if len(FConflitP[pointIndex]) == 1:
#faceIndex=FConflitP[pointIndex][0]
face=visibleFaces[0]
validFaces.append(Face(self.pointSet,pointIndex,face.pIndex1,face.pIndex2))  
validFaces.append(Face(self.pointSet,pointIndex,face.pIndex2,face.pIndex3)) 
validFaces.append(Face(self.pointSet,pointIndex,face.pIndex3,face.pIndex1)) 
elif len(FConflitP[pointIndex]) > 1 :
boundaryPoint=[]
for x, faceSee in enumerate(visibleFaces):
boundaryPoint+=faceSee.pointList
print(boundaryPoint)
boundaryPoint=list(set(boundaryPoint))
print("邊界點:",point,boundaryPoint) 
print(self.__counterclockwise(point,boundaryPoint))
for i in range(len(boundaryPoint)):
if i+1 < len(boundaryPoint):
validFaces.append(Face(self.pointSet,pointIndex,boundaryPoint[i],boundaryPoint[i+1]))
else:
validFaces.append(Face(self.pointSet,pointIndex,boundaryPoint[i],boundaryPoint[0]))