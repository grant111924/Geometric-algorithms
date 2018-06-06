import numpy as np 

class Face(object):
    def __init__ (self,pointSet,pIndex1,pIndex2,pIndex3):
        self.pointSet=pointSet
        self.pIndex1=pIndex1
        self.pIndex2=pIndex2
        self.pIndex3=pIndex3
        self.pointList=[pIndex1,pIndex2,pIndex3]
        self.a,self.b,self.c,self.d=None,None,None,None
        
        self.__computePlane()
        
    def isVisible(self, pointR):
        return (self.a*pointR[0] + self.b*pointR[1]+ self.c*pointR[2]+self.d)

    def getCentroid(self):
        p1=self.pointSet[self.pIndex1]
        p2=self.pointSet[self.pIndex2]
        p3=self.pointSet[self.pIndex3]
        self.result=np.array([(p1[0]+p2[0]+p3[0])/3,(p1[1]+p2[1]+p3[1])/3,(p1[2]+p2[2]+p3[2])/3])

    def flip(self):
        t=self.pIndex1
        self.pIndex1=self.pIndex2
        self.pIndex2=t
        self.__computePlane()

    def __computePlane(self):
        vector1=self.pointSet[self.pIndex1]
        vector2=self.pointSet[self.pIndex2]
        vector3=self.pointSet[self.pIndex3]
        self.a = vector1[1]*(vector2[2]-vector3[2]) + vector2[1]*(vector3[2]-vector1[2]) + vector3[1]*(vector1[2]-vector2[2])
        self.b = vector1[2]*(vector2[1]-vector3[1]) + vector2[2]*(vector3[1]-vector1[1]) + vector3[2]*(vector1[1]-vector2[1])
        self.c = vector1[0]*(vector2[1]-vector3[1]) + vector2[0]*(vector3[1]-vector1[1]) + vector3[0]*(vector1[1]-vector2[1])
        self.d = -((vector1[0]*(vector2[1]*vector3[2]-vector3[1]*vector2[2])) + \
                    (vector2[0]*(vector3[1]*vector1[2]-vector1[1]*vector3[2])) + \
                    (vector3[0]*(vector1[1]*vector2[2]-vector2[1]*vector1[2])))
    