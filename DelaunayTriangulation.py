# -*- coding: utf-8 -*-
"""
Created on Wed May  9 13:43:14 2018

@author: wong
"""
import cv2 
import json 
import numpy as np 
import matplotlib.pyplot as plt  
import numpy as np
from matplotlib.patches import Circle

class DelaunayTriangulation(object):
    def __init__(self,image_size=(40,40),count=10):
        self.image_size=image_size
        self.points=np.random.rand(count,2) 
        self.plt=plt
    def __supertriangle(self,vertices):
        xmin=1
        ymin=1
        xmax=0
        ymax=0
        for x in vertices:
            if x[0]<xmin:
                xmin = x[0]
            if (x[0]>xmax):
                xmax = x[0]  
            if(x[1]<ymin):
                ymin = x[1]
            if (x[1]>ymax):
                ymax = x[1]  
        dx = xmax -xmin
        dy = ymax -ymin
        Extenx=max(0.1*dy,0.1*dx)
        Exteny=min(0.1*dy,0.1*dx)
        
        return  [ [xmin- dx/2-Extenx, ymin-Exteny],
        [xmax-dx/2, ymax+dy],
        [xmax + dx/2+Extenx,ymin-Exteny]
        ]
    def __judge_circle_point_relation(self,center, r, point):
            # Input:
            #   (x,y), r, (x,y)
            x1, y1 = center 
            x2, y2 = point 
            if (x2-x1)**2 + (y2-y1)**2 <= r**2:
                return 2
            elif x2 > x1:
                return 0
            else:
                return 1
    def __cal_circum_circle(self,triangle):
            # Input:
            #   (3,2)
            # Output:
            #   (x,y), r
            x1, x2, x3 = triangle[:, 0]
            y1, y2, y3 = triangle[:, 1]
            a = np.sqrt(np.sum((triangle[0, :] - triangle[1, :])**2))
            b = np.sqrt(np.sum((triangle[0, :] - triangle[2, :])**2))
            c = np.sqrt(np.sum((triangle[1, :] - triangle[2, :])**2))
            S = (1/2)*a*b*np.sqrt(1 - ((a**2 + b**2 - c**2)/(2*a*b))**2)
            if S == 0:
                r = 0
                x, y = x1, y1
            else:
                r = (a*b*c)/(4*S)
                x = np.linalg.det([[x1**2 + y1**2, y1, 1],[x2**2 + y2**2, y2, 1],[x3**2 + y3**2, y3, 1]])/(2*np.linalg.det([[x1, y1, 1],[x2, y2, 1],[x3, y3, 1]]))
                y = np.linalg.det([[x1, x1**2 + y1**2, 1],[x2, x2**2 + y2**2, 1],[x3, x3**2 + y3**2, 1]])/(2*np.linalg.det([[x1, y1, 1],[x2, y2, 1],[x3, y3, 1]]))

            return (x, y), r
    def __draw2(self,triangles,verticies):
        res = np.zeros((len(triangles), 3, 2))
        for ind, tri_ind in enumerate(triangles):
                res[ind] = verticies[list(tri_ind)]
        result2 = res.reshape(res.shape[0]*res.shape[1],res.shape[2])
        self.plt.triplot(result2[:,0], result2[:,1],color='r') # 绘制三角格网  
        #self.plt.plot(result2[:,0], result2[:,1], 'o') # 绘制點
       # self.plt.pause(0.1)
    def cal_delaunay_triangle(self):
            #輸入二維座標拆成 h,w
            h, w = self.image_size
            verticies=self.points
            origin_length = verticies.shape[0]
            
            verticies = verticies.copy() 
            triangles, temp_triangles = set(), set()
            indices = np.arange(verticies.shape[0])
            indices = indices[np.argsort(verticies[:, 0])]

            # super triangle 
            a, b, c = self.__supertriangle(verticies)
            verticies = np.concatenate([verticies, np.array([a,b,c])], axis=0)
            indices = list(indices)
            [indices.append(len(indices)) for i in range(3)]
            triangles.add((indices[-3], indices[-1], indices[-2])) # a,c,b
            temp_triangles.add((indices[-3], indices[-1], indices[-2])) # a,c,b
        
            
            # main loop 
            for ind in indices[:-3]:#抓所有點除了最大三小形
                edge_buffer = set()
                self.plt.clf()
                plt.plot(verticies[:,0], verticies[:,1], 'o') 
                self.__draw2(triangles,verticies)
                self.plt.pause(0.5)
                buf_temp_triangles = temp_triangles.copy()
                
                for tri_ind in temp_triangles:
                    tri = verticies[list(tri_ind)]
                    self.__draw2(temp_triangles,verticies)
                    center, r = self.__cal_circum_circle(tri)
                    x1,y1=center
                    print(x1,y1,r)
                    i1,i2 = verticies[ind, :]
                    self.plt.plot(i1, i2, 'o',color='r')
                    
                    
                    res = self.__judge_circle_point_relation(center, r, verticies[ind, :])
                
                    if res == 0:#圓的右邊
                        triangles.add(tri_ind)
                        buf_temp_triangles.remove(tri_ind)
                    elif res == 1:#圓外
                        continue 
                    else: # a, c, b => (a,c), (a,b), (c,b)在圓內存三邊 如果邊內已經存在則刪除
                        if (tri_ind[0], tri_ind[1]) not in edge_buffer:
                            edge_buffer.add((tri_ind[0], tri_ind[1]))
                        else:
                            continue
                        if (tri_ind[0], tri_ind[2]) not in edge_buffer:
                            edge_buffer.add((tri_ind[0], tri_ind[2]))
                        else:
                            continue
                        if (tri_ind[1], tri_ind[2]) not in edge_buffer:
                            edge_buffer.add((tri_ind[1], tri_ind[2]))
                        else:
                            continue
                        buf_temp_triangles.remove(tri_ind)
                plt.pause(0.5)    
                
                for edge in edge_buffer:#把邊轉換成三角形 
                    tmp_ind = np.array([ind, edge[0], edge[1]])
                    points = np.array([verticies[tmp_ind[0]], verticies[tmp_ind[1]], verticies[tmp_ind[2]]])
                    tmp_ind = tmp_ind[np.argsort(points[:, 0])]
                    buf_temp_triangles.add((tmp_ind[0], tmp_ind[1], tmp_ind[2]))
                
                temp_triangles = buf_temp_triangles
            
            triangles = triangles.union(temp_triangles)#合併
            self.plt.clf()
            self.plt.plot(verticies[:,0], verticies[:,1], 'o') 
            self.__draw2(triangles,verticies)
            self.plt.pause(2)

            final_triangles = triangles.copy()
            for tri_ind in triangles:
                if np.sum(np.array(tri_ind) >= origin_length) > 0:
                    final_triangles.remove(tri_ind)
                    
            res = np.zeros((len(final_triangles), 3, 2))
            self.plt.clf()
            self.plt.plot(verticies[:,0], verticies[:,1], 'o') # 绘制10这十个离散点 
            self.__draw2(final_triangles,verticies)
            self.plt.pause(0.5)
            self.plt.show()  

if __name__ == "__main__": 
    DelaunayTriangulation().cal_delaunay_triangle()
