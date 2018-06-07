from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from face import Face
import random
from tqdm import tqdm
import time
import networkx as nx
from networkx.algorithms import bipartite

class ConvexHull3D(object):
    def __init__(self,low=1,high=10,size=(5,3)):
        self.pointSet=np.random.randint(low,high,size=size)
        """count=25
        pointSet=np.zeros((count,3))
        for i in range(count):
            radius= (5 + np.random.random_sample())* 5
            theta= np.random.random_sample()*2* np.pi
            phi=np.random.random_sample() * np.pi
            pointSet[i][0]=np.cos( theta ) * np.sin( phi ) * radius
            pointSet[i][1]=np.cos( phi ) * radius
            pointSet[i][2]=np.sin( theta ) * np.sin( phi ) * radius
        self.pointSet=pointSet"""
        self.plt=plt
    def process(self):
        #四面體成形
        self.__find_tetrahedron()
        self.validFaces=self.tetrahedron
        #畫初始四面體
        self.result=[]
        for finalIndex, finalFace in enumerate(self.validFaces):
            self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
        
        
        #建立graph
        #pointIndexList = [i for i in range(len(self.pointSet))]
        #faceIndexList = [validFaces[i].pointList for i in range(len(validFaces))]
        #初始化 graph
        self.visiblePairList=[]
        self.FConflitP=[[] for i in range(len(self.pointSet))]
        self.PConflitF=[[] for f in range(len(self.validFaces))]

        
        """for fIndex , face in enumerate(self.validFaces):
            for pIndex, point in enumerate(self.pointSet):
                if pIndex > 3:
                    if np.sign(face.isVisible(self.centerPoint)) != np.sign(face.isVisible(point)):
                        self.visiblePairList.append((pIndex,fIndex))"""
        for pIndex, point in enumerate(self.pointSet):
            print("pointIndex:%d point: %s"%(pIndex,point))
            if  pIndex > 3:
                for fIndex,face in enumerate(self.validFaces):
                    print("centerPoint :",face.isVisible(self.centerPoint))
                    print("this point :",face.isVisible(point))
                    if np.sign(face.isVisible(self.centerPoint)) != np.sign(face.isVisible(point)):
                         self.visiblePairList.append((pIndex,fIndex))

        self.__plot()
            
        for pairIndex, pair in enumerate(self.visiblePairList):
            self.FConflitP[pair[0]].append(pair[1])
            self.PConflitF[pair[1]].append(pair[0])
        
        print("visiblePairList",self.visiblePairList)
        print("FConflitP",self.FConflitP)
        print("PConflitF",self.PConflitF)

        """
        for pointIndex , point in enumerate(self.pointSet):
            if  pointIndex>3 and len(self.FConflitP[pointIndex]) != 0:
                print("visiblePairList",self.visiblePairList)
                print("FConflitP",self.FConflitP)
                print("PConflitF",self.PConflitF)
                
                #先刪除 從validFaces中 可以看到的面
                visibleFaces=[]
                for faceValidIndex, faceValid in enumerate(self.validFaces):
                    for x, faceSeeIndex in enumerate(self.FConflitP[pointIndex]):
                        if faceValidIndex == faceSeeIndex : 
                            visibleFaces.append(faceValid)
                for faceVisibleIndex, faceVisible in enumerate(visibleFaces):
                    if faceVisible in self.validFaces:
                        self.validFaces.remove(faceVisible)

                boundaryPoint=[]      
                for x, faceSee in enumerate(visibleFaces):
                    boundaryPoint+=faceSee.pointList
                #print(boundaryPoint)
                boundaryPoint=list(set(boundaryPoint)) # 去除重複邊界點
                #print("邊界點:",point,boundaryPoint) 
                #print('排序邊界點:',self.__counterclockwise(point,boundaryPoint))
                sortBoundaryPoint=boundaryPoint
                #形成新的面 
                for i in range(len(sortBoundaryPoint)):
                    if i+1 < len(sortBoundaryPoint):#這個面 跟 周遭是否共面
                        edge=[sortBoundaryPoint[i],sortBoundaryPoint[i+1]]
                        #print(edge)
                        tmpFace=Face(self.pointSet,pointIndex,edge[0],edge[1])
                        tmpFacePlane=tmpFace.getPlane()

                        for fIndex, face in enumerate(self.validFaces):
                            for eIndex, e in enumerate(face.edgeList):
                                if e[0] in edge and e[1]  in edge:
                                    aroundFace=face
                                    aroundFacePlane=aroundFace.getPlane()      
                                    if np.all(aroundFacePlane*len(tmpFacePlane) - tmpFacePlane*len(aroundFacePlane)) == 0:
                                        print("共面")
                                    else:
                                        print("加入")
                                        self.validFaces.append(tmpFace)
                    else:
                        edge=[sortBoundaryPoint[i],sortBoundaryPoint[0]]
                        tmpFace=Face(self.pointSet,pointIndex,sortBoundaryPoint[i],sortBoundaryPoint[0])
                        tmpFacePlane=tmpFace.getPlane()

                        for fIndex, face in enumerate(self.validFaces):
                            for eIndex, e in enumerate(face.edgeList):
                                if e[0] in edge and e[1]  in edge:
                                    aroundFace=face
                                    aroundFacePlane=aroundFace.getPlane()      
                                    if np.all(aroundFacePlane*len(tmpFacePlane) - tmpFacePlane*len(aroundFacePlane)) == 0:
                                        print("共面")
                                    else:
                                        print("加入")
                                        self.validFaces.append(tmpFace)
                    self.result=[]
                    for finalIndex, finalFace in enumerate(self.validFaces):
                        self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
                    self.__plot()  
                    print(self.result) 
                self.__update(pointIndex)
        """
                     
                
                
                
                


                
                
        """
        self.result=[]
        for finalIndex, finalFace in enumerate(self.validFaces):
            self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
        self.__plot()  
        print(self.result)"""
        
            


                

    def __find_tetrahedron(self):
        pointSet=self.pointSet
        while True:
            vectorAB=pointSet[0]-pointSet[1]
            vectorAC=pointSet[0]-pointSet[2]
            if np.sum(np.cross(vectorAB,vectorAC)!=0):
                face=Face(pointSet,0,1,2)
                if face.isVisible(pointSet[3])!=0:
                    face1=Face(pointSet,3,face.pIndex1,face.pIndex2)
                    face2=Face(pointSet,3,face.pIndex2,face.pIndex3)
                    face3=Face(pointSet,3,face.pIndex3,face.pIndex1)
                    self.tetrahedron=[face,face1,face2,face3]
                    self.centerPoint=self.__centroid(3,face)
                    break
            else:self.pointSet=np.random.shuffle(pointSet)
       
    def __centroid(self,index,face):
        p=self.pointSet[index]
        p1=self.pointSet[face.pIndex1]
        p2=self.pointSet[face.pIndex2]
        p3=self.pointSet[face.pIndex3]
        return  np.array( [(p[0]+p1[0]+p2[0]+p3[0])/4,(p[1]+p1[1]+p2[1]+p3[1])/4,(p[2]+p1[2]+p2[2]+p3[2])/4])

    def __update(self,index):
        self.visiblePairList.clear()
        for pIndex, point in enumerate(self.pointSet):
            if  pIndex > 3:
                for fIndex,face in enumerate(self.validFaces):
                    if np.sign(face.isVisible(self.centerPoint)) != np.sign(face.isVisible(point)):
                         self.visiblePairList.append((pIndex,fIndex))
        
        self.FConflitP=[[] for i in range(len(self.pointSet))]
        self.PConflitF=[[] for f in range(len(self.validFaces))]
        for pairIndex, pair in enumerate(self.visiblePairList):
            self.FConflitP[pair[0]].append(pair[1])
            self.PConflitF[pair[1]].append(pair[0])
      
        
    def __counterclockwise(self,p,bList):
        centerPoint=np.array([0,0,0])
        for x, pindex in enumerate(bList):
            centerPoint+=self.pointSet[pindex]
        centerPoint=centerPoint/len(bList)
        
        sortList=[]
        for index, pointIndex in enumerate(bList):
            if index== 0:
                tmp=self.pointSet[pointIndex]
                sortList.append((0,pointIndex))
            else: 
                x=np.dot(centerPoint-p,np.cross(tmp-centerPoint,self.pointSet[pointIndex]-centerPoint))
                sortList.append((x,pointIndex))
        sortIndexList=sorted(sortList,key=lambda s: s[0])
        result=[]
        for index,item in enumerate(sortIndexList):
            result.append(item[1])
        return result

    def __plot(self):
        fig=self.plt.figure()
        ax=fig.add_subplot(111,projection='3d')
        xs=self.pointSet[:,0]
        ys=self.pointSet[:,1] 
        zs=self.pointSet[:,2]
        ax.scatter(xs,ys,zs,c='b',marker='o')
        ax.scatter(xs,ys,zs,c='b',marker='o')
        ax.scatter(self.centerPoint[0],self.centerPoint[1],self.centerPoint[2],c="g",marker="o")
        for x, y, z in zip(xs, ys, zs):
            label = '(%d, %d, %d)' % (x, y, z)
            ax.text(x, y, z, label)

        for index ,face in enumerate(self.result):
            xv=[self.pointSet[face[0]],self.pointSet[face[1]],self.pointSet[face[2]]]
            ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),arrowprops=dict(facecolor='black', shrink=0.05),)
            ax.plot ( [ xv[0][0], xv[1][0] ], [ xv[0][1], xv[1][1] ], [ xv[0][2],xv[1][2] ], 'r' )
            ax.plot ( [ xv[0][0], xv[2][0] ], [ xv[0][1], xv[2][1] ], [ xv[0][2], xv[2][2] ], 'r' )
            ax.plot ( [ xv[1][0], xv[2][0] ], [ xv[1][1], xv[2][1] ], [ xv[1][2], xv[2][2] ], 'r' )
        plt.show()
if __name__ == "__main__":
    c=ConvexHull3D()
    c.process()