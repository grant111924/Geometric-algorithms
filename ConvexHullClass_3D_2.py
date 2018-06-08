from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from face import Face
import random
from tqdm import tqdm
import time

class ConvexHull3D(object):
    def __init__(self,low=1,high=100,size=(10,3)):
        self.pointSet=np.random.randint(low,high,size=size)
        self.plt=plt
    def process(self):
        #四面體成形
        self.__find_tetrahedron()
        self.validFaces=self.tetrahedron
        #畫初始四面體
        self.result=[]
        for finalIndex, finalFace in enumerate(self.validFaces):
            self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
        self.__plot()



        
        for pIndex, point in enumerate(self.pointSet):
            print("pointIndex:%d point: %s"%(pIndex,point))
            if  pIndex > 3:
                print("validFaces 開始",self.validFaces)
                # 找出該點 可以見到的面 (visibleFaces)
                visibleFaces=[]
                for fIndex,face in enumerate(self.validFaces):
                    if np.sign(face.isVisible(self.centerPoint)) != np.sign(face.isVisible(point)):
                        visibleFaces.append(face)
                print("visibleFaces",visibleFaces)

                #收集所有面的edge
                
                # 刪除 所有看到的面的邊
                for vF, vFace in enumerate(self.validFaces):
                    if vFace in visibleFaces:
                        self.validFaces.remove(vFace)
                print("validFaces 刪除後",self.validFaces)
                self.result=[]
                for finalIndex, finalFace in enumerate(self.validFaces):
                    self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
                self.__plot()
                break
            



                

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
    