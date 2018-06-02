from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from face import Face
import random
from tqdm import tqdm
class ConvexHull3D(object):
    def __init__(self,low=0,high=1,size=(15,3)):
        #self.pointSet=np.random.randint(low,high,size=size)
        count=15
        pointSet=np.zeros((count,3))
        for i in range(count):
            radius= (5 + np.random.random_sample())* 5
            theta= np.random.random_sample()*2* np.pi
            phi=np.random.random_sample() * np.pi
            pointSet[i][0]=np.cos( theta ) * np.sin( phi ) * radius
            pointSet[i][1]=np.cos( phi ) * radius
            pointSet[i][2]=np.sin( theta ) * np.sin( phi ) * radius
        """self.pointSet=np.array([ np.cos( theta ) * np.sin( phi ) * radius,\
                                np.cos( phi ) * radius, \
                                np.sin( theta ) * np.sin( phi ) * radius ])"""
        self.pointSet=pointSet
        self.plt=plt
        
        

       
    def process(self):
        
        firstFace=Face(self.pointSet,0,1,2)
        firstFaceCentroid=self.__centroid(3,firstFace)
        if firstFace.isVisible(firstFaceCentroid):firstFace.flip()
        
        face1=Face(self.pointSet,3,firstFace.pIndex1,firstFace.pIndex2)
        if face1.isVisible(firstFaceCentroid):face1.flip()

        face2=Face(self.pointSet,3,firstFace.pIndex2,firstFace.pIndex3)
        if face2.isVisible(firstFaceCentroid):face2.flip()

        face3=Face(self.pointSet,3,firstFace.pIndex3,firstFace.pIndex1)
        if face3.isVisible(firstFaceCentroid):face3.flip()

        validFaces=[firstFace,face1,face2,face3]
        visibleFaces=[]
        tmpFaces=[]
        print("validFaces:",validFaces)
        for index , point in enumerate(self.pointSet):
            if index > 3:
                visibleFaces=[]
                for fIndex, face in enumerate(validFaces):
                    if face.isVisible(point):visibleFaces.append(face)
        
            if len(visibleFaces) == 0:continue
            
            #delete all visible faces from the validFaces list
            for fIndex,face in enumerate(visibleFaces):
                if face in validFaces: validFaces.remove(face)
            
            # if only one face is visible  create 3 faces
            if len(visibleFaces) == 1:
                face=visibleFaces[0]
                validFaces.append(Face(self.pointSet,index,face.pIndex1,face.pIndex2))
                validFaces.append(Face(self.pointSet,index,face.pIndex2,face.pIndex3))
                validFaces.append(Face(self.pointSet,index,face.pIndex3,face.pIndex1))
                continue
            # create all possible  new faces from the visibleFacs list
            tmpFaces=[]
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
                            face=None
                            break
                if tmpFace != None :
                    validFaces.append(tmpFace)
            
        self.reuslt=[]
        for finalIndex, finalFace in enumerate(validFaces):
            self.reuslt.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
        
            
        """if finalIndex != 0:
                for rIndex, rFace in enumerate(self.reuslt):
                    if finalFace.pIndex1  in  rFace and finalFace.pIndex2  in  rFace and finalFace.pIndex3  in  rFace: continue
                    else: self.reuslt.append([finalFace.pIndex1,finalFace.pIndex2,finalFace.pIndex3])
            else:"""
        #print("visibleFaces:",visibleFaces)
        #print("validFaces:",validFaces)
        #self.reuslt=list(set(self.reuslt))
        print("result :",self.reuslt)

    def plot(self):
        fig=self.plt.figure()
        ax=fig.add_subplot(111,projection='3d')
        xs=self.pointSet[:,0]
        ys=self.pointSet[:,1] 
        zs=self.pointSet[:,2]
        ax.scatter(xs,ys,zs,c='b',marker='o')
        for index ,face in enumerate(self.reuslt):
            xv=[self.pointSet[face[0]],self.pointSet[face[1]],self.pointSet[face[2]]]
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
    c=ConvexHull3D()
    c.process()
    c.plot()