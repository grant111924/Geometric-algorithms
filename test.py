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
        