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
    def __init__(self,low=0,high=5,size=(10,3)):
        self.pointSet=np.random.randint(low,high,size=size)
        self.plt=plt
    def process(self):
        #四面體成形
        self.__find_tetrahedron()
        validFaces=self.tetrahedron
        #畫初始四面體
        self.result=[]
        for finalIndex, finalFace in enumerate(validFaces):
            self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
        self.__plot()
        
        #建立graph
        pointIndexList = [i for i in range(len(self.pointSet))]
        faceIndexList = [validFaces[i].pointList for i in range(len(validFaces))]
        print(faceIndexList)
        #初始化 graph
        visiblePairList=[]
        FConflitP=[[] for i in range(len(self.pointSet))]
        PConflitF=[[] for f in range(len(validFaces))]
        for faceIndex, face in enumerate(validFaces):
            FourPointSet=[i for i in range(4)]
            FourPointSet.remove(face.pIndex1)
            FourPointSet.remove(face.pIndex2)
            FourPointSet.remove(face.pIndex3)
            p=FourPointSet[0]
            for i in range(4,len(pointIndexList)):
                if np.sign(face.isVisible(self.pointSet[p])) != np.sign(face.isVisible(self.pointSet[i])):
                   visiblePairList.append((i,faceIndex))
        for pairIndex, pair in enumerate(visiblePairList):
            FConflitP[pair[0]].append(pair[1])
            PConflitF[pair[1]].append(pair[0])
        print(FConflitP)
        print(PConflitF)
        """for pointIndex, point in enumerate(self.pointSet):
            if pointIndex > 3 and len(FConflitP[pointIndex]) != 0:
                print(faceIndexList[FConflitP[pointIndex][0]])
                if len(FConflitP[pointIndex]) == 1 :
                    validFaces.append(Face(self.pointSet,pointIndex,face.pIndex1,face.pIndex2))
                    validFaces.append(Face(self.pointSet,pointIndex,face.pIndex2,face.pIndex3))
                    validFaces.append(Face(self.pointSet,pointIndex,face.pIndex3,face.pIndex1))
                    faceIndexList= [validFaces[i].pointList for i in range(len(validFaces))]
            self.result=[]
            for finalIndex, finalFace in enumerate(validFaces):
                self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
            self.__plot()  """

        
            


                

    def __find_tetrahedron(self):
        pointSet=self.pointSet
        while True:
            vectorAB=pointSet[0]-pointSet[1]
            vectorAC=pointSet[0]-pointSet[2]
            if np.sum(np.cross(vectorAB,vectorAC)!=0):
                face=Face(self.pointSet,0,1,2)
                if face.isVisible(pointSet[3])!=0:
                    face1=Face(pointSet,3,face.pIndex1,face.pIndex2)
                    face2=Face(pointSet,3,face.pIndex2,face.pIndex3)
                    face3=Face(pointSet,3,face.pIndex3,face.pIndex1)
                    self.tetrahedron=[face,face1,face2,face3]
                    break
            else:self.pointSet=np.random.shuffle(pointSet)
       


    def __plot(self):
        fig=self.plt.figure()
        ax=fig.add_subplot(111,projection='3d')
        xs=self.pointSet[:,0]
        ys=self.pointSet[:,1] 
        zs=self.pointSet[:,2]
        ax.scatter(xs,ys,zs,c='b',marker='o')
        
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