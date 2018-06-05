from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from face import Face
import random
from tqdm import tqdm
import time
class ConvexHull3D(object):
    def __init__(self,low=0,high=5,size=(5,3)):
        self.pointSet=np.random.randint(low,high,size=size)
        """count=10
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
        firstFace=Face(self.pointSet,0,1,2)
        self.firstFaceCentroid=self.__centroid(3,firstFace)
        print("normal firstFace point:",[firstFace.pIndex1,firstFace.pIndex2,firstFace.pIndex3])
        if firstFace.isVisible(self.firstFaceCentroid):firstFace.flip()
        print("normal firstFace:",[firstFace.a,firstFace.b,firstFace.c])
        print("normal firstFace point:",[firstFace.pIndex1,firstFace.pIndex2,firstFace.pIndex3])

        
        face1=Face(self.pointSet,3,firstFace.pIndex1,firstFace.pIndex2)
        print("normal face1 翻轉前:",[face1.a,face1.b,face1.c])
        print("normal face1 point:",[face1.pIndex1,face1.pIndex2,face1.pIndex3])
        if face1.isVisible(self.firstFaceCentroid):face1.flip()
        print("normal face1:",[face1.a,face1.b,face1.c])
        print("normal face1 point:",[face1.pIndex1,face1.pIndex2,face1.pIndex3])
        if not face1.isVisible(self.firstFaceCentroid) : print("翻轉成功")
        
        face2=Face(self.pointSet,3,firstFace.pIndex2,firstFace.pIndex3)
        print("normal face2 翻轉前:",[face2.a,face2.b,face2.c])
        print("normal face2 point:",[face2.pIndex1,face2.pIndex2,face2.pIndex3])
        if face2.isVisible(self.firstFaceCentroid):face2.flip()
        print("normal face2:",[face2.a,face2.b,face2.c])
        print("normal face2 point:",[face2.pIndex1,face2.pIndex2,face2.pIndex3])
        if not face2.isVisible(self.firstFaceCentroid) : print("翻轉成功")
       
        face3=Face(self.pointSet,3,firstFace.pIndex3,firstFace.pIndex1)
        print("normal face3 翻轉前:",[face3.a,face3.b,face3.c])
        print("normal face3 point:",[face3.pIndex1,face3.pIndex2,face3.pIndex3])
        if face3.isVisible(self.firstFaceCentroid):face3.flip()
        print("normal face3:",[face3.a,face3.b,face3.c])
        print("normal face3 point:",[face3.pIndex1,face3.pIndex2,face3.pIndex3])
        if not face3.isVisible(self.firstFaceCentroid) : print("翻轉成功")

        validFaces=[firstFace,face1,face2,face3]
        visibleFaces=[]
        tmpFaces=[]
        print("validFaces:",validFaces)
        print("firstFaceCentroid",self.firstFaceCentroid)
        self.result=[]
        for finalIndex, finalFace in enumerate(validFaces):
            self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
        self.__plot()

        for index , point in enumerate(self.pointSet):
            if index > 3:
                visibleFaces.clear()
                print(point)
                for fIndex, face in enumerate(validFaces):
                    print(face.a*point[0] + face.b*point[1]+ face.c*point[2]+face.d)
                    if face.isVisible(point):
                        print("face:",face)
                        visibleFaces.append(face)
                print("pointIndex: %d,visibleFaces: %s"%(index,visibleFaces))
            
                if len(visibleFaces) == 0:continue
                
                #delete all visible faces from the validFaces list
                for fIndex,face in enumerate(visibleFaces):
                    if face in validFaces: 
                        print(face)
                        print("removeFace:",[face.pIndex1,face.pIndex2,face.pIndex3])
                        validFaces.remove(face)
                
                # if only one face is visible  create 3 faces
                if len(visibleFaces) == 1:
                    face=visibleFaces[0]
                    validFaces.append(Face(self.pointSet,index,face.pIndex1,face.pIndex2))
                    validFaces.append(Face(self.pointSet,index,face.pIndex2,face.pIndex3))
                    validFaces.append(Face(self.pointSet,index,face.pIndex3,face.pIndex1))
                    continue
                # create all possible  new faces from the visibleFacs list
                tmpFaces.clear()
                for fIndex, face in enumerate(visibleFaces):
                    tmpFaces.append(Face(self.pointSet,index,face.pIndex1,face.pIndex2))
                    tmpFaces.append(Face(self.pointSet,index,face.pIndex2,face.pIndex3))
                    tmpFaces.append(Face(self.pointSet,index,face.pIndex3,face.pIndex1))
                # search  if there is a point in front of the face
                # this means the face is not a boundary face 
                for tIndex ,tmpFace in enumerate(tmpFaces):
                    for oIndex, otherFace in enumerate(tmpFaces):
                        if tIndex != oIndex:
                            otherFace.getCentroid()
                            if tmpFace.isVisible(otherFace.result):
                                tmpFace=None
                                break
                    if tmpFace != None and tmpFace not in validFaces  :
                        validFaces.append(tmpFace)
                
                print("validFaces:",len(validFaces))
                self.result=[]
                for finalIndex, finalFace in enumerate(validFaces):
                    self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
                self.__plot()
                    
         

        self.result=[]
        self.pointResult=[]
        for finalIndex, finalFace in enumerate(validFaces):
            self.result.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
            self.pointResult.append(finalFace.pIndex1)
            self.pointResult.append(finalFace.pIndex2)
            self.pointResult.append(finalFace.pIndex3)
        self.pointResult=list(set(self.pointResult))
        #print("visibleFaces:",visibleFaces)
        #print("validFaces:",validFaces)
        #self.reuslt=list(set(self.reuslt))
        print("result :",self.result)
        print("pointResult :",self.pointResult)
        self.__plot()

    def __plot(self):
        fig=self.plt.figure()
        ax=fig.add_subplot(111,projection='3d')
        xs=self.pointSet[:,0]
        ys=self.pointSet[:,1] 
        zs=self.pointSet[:,2]
        ax.scatter(xs,ys,zs,c='b',marker='o')
        ax.scatter(self.firstFaceCentroid[0],self.firstFaceCentroid[1],self.firstFaceCentroid[2],c="g",marker="o")
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


    def __centroid(self,index,face):
        p=self.pointSet[index]
        p1=self.pointSet[face.pIndex1]
        p2=self.pointSet[face.pIndex2]
        p3=self.pointSet[face.pIndex3]
        return  np.array( [(p[0]+p1[0]+p2[0]+p3[0])/4,(p[1]+p1[1]+p2[1]+p3[1])/4,(p[2]+p1[2]+p2[2]+p3[2])/4])

if __name__ == '__main__':

    tStart = time.time()
    c=ConvexHull3D()
    c.process()
    tEnd = time.time()
    #c.plot()
    print( "It cost %f sec" % (tEnd - tStart))
    