# -*- coding: utf-8 -*-
"""
icosahedron chess
"""

from Tkinter import *
import numpy
import xlrd
import xlwt
import tkMessageBox

N = 13#每边划分成N个小三角形

M = 13#number of gamers

gamers = numpy.array(range(M))

d_unit = 10#单个小三角边长

d = [d_unit]#作图坐标扩大倍率

Mat = numpy.zeros((12,12),dtype=int)#顶点的邻接矩阵

f = open('relation_matrix.txt')               #打开数据文件文件
lines = f.readlines()           #把全部数据文件读到一个列表lines中
Mat_row = 0                       #表示矩阵的行，从0行开始
for line in lines:              #把lines中的数据逐行读取出来
    s = line.strip('\n').split('\t')      #处理逐行数据：strip表示把头尾的'\n'去掉，split表示以空格来分割行数据，然后把处理后的行数据返回到list列表中
    Mat[Mat_row:] = s[0:12]                    #把处理后的数据放到方阵A中。list[0:3]表示列表的0,1,2列数据放到矩阵A中的A_row行
    Mat_row+=1                                #然后方阵A的下一行接着读

face_set = []#得到每个面的三个顶点
for vertex_1 in range(12):
    for vertex_2 in range(12)[vertex_1+1:]:
        if Mat[vertex_1,vertex_2]:
            for vertex_3 in range(12)[vertex_2+1:]:
                if Mat[vertex_1,vertex_3] and Mat[vertex_2,vertex_3]:
                    face_set.append([vertex_1,vertex_2,vertex_3])
     

def get_local_coordinate(n):#获得一个顶点局部的5条坐标轴
    mid_vertex = n  #0,1,2,3,4,5,6,7,8,9,10,11           
    
    local_graph = []            
    
    local_graph_face = []#局部图中的面
    
    local_graph_axis = []#局部图相邻的轴
    
    for face in face_set:
        if mid_vertex in face:
            local_graph_face.append(face[:])
    
    for face in local_graph_face:
        face.remove(mid_vertex)
    
    end = local_graph_face[0][0]
    local_graph_axis.append(end)
    temp = 1
    while temp<5:
        for face in local_graph_face:
            if end in face:
                face.remove(end)
                end = face[0]
                local_graph_axis.append(end)
                face.remove(end)
                temp = temp + 1
    
    return local_graph_axis





class Point(object):#格对象
    def __init__(self,vertice_A,vertice_B,vertice_C,x,y,z,owner):
        self.vertice_A = int(vertice_A)
        self.vertice_B = int(vertice_B)
        self.vertice_C = int(vertice_C)
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.owner = int(owner)#格被哪个玩家占领
    def valid(self):
        flag = True
        if not((self.x+self.y+self.z==2*N+2)or(self.x+self.y+self.z==2*N+1)):
            flag = False
        if not(self.x<=N and self.x>=1):
            flag = False
        if not(self.y<=N and self.y>=1):
            flag = False
        if not(self.z<=N and self.z>=1):
            flag = False
        if self.vertice_B not in get_local_coordinate(self.vertice_A):
            flag = False
        if self.vertice_C not in get_local_coordinate(self.vertice_A):
            flag = False
        if self.vertice_B not in get_local_coordinate(self.vertice_C):
            flag = False
        return flag
    def point_compare_position(self,p2):#比较两个点的位置是否一样
        flag = False
        p1 = self
        symm = ['012','021','102','120','201','210']
        p1 = [p1.vertice_A,p1.vertice_B,p1.vertice_C,p1.x,p1.y,p1.z]
        p2 = [p2.vertice_A,p2.vertice_B,p2.vertice_C,p2.x,p2.y,p2.z]
        for s in symm:
            temp = []
            for i in range(3):
                temp.append(p2[int(s[i])]) 
            for i in range(3):
                temp.append(p2[int(s[i])+3])
            if temp == p1:
                flag = True
        return flag
            
    
class Local_Point(Point):#局部坐标
    def __init__(self,vertice_A,vertice_B,vertice_C,x,y,z,owner,local_x,local_y):
        Point.__init__(self,vertice_A,vertice_B,vertice_C,x,y,z,owner)
        self.local_x=local_x
        self.local_y=(local_y - 1)%(6*(2*local_x - 1)) + 1
        triangle_vertice = []
        if (local_y <= 2 * local_x) and (local_y > 0):
            if local_y % 2:
                triangle_vertice = [[(local_y - 1)/2,local_x - 1],[(local_y - 1)/2,local_x],[(local_y + 1)/2,local_x]]
            else:
                triangle_vertice = [[local_y / 2,local_x - 1],[local_y / 2,local_x],[local_y/2-1,local_x-1]]
        if (local_y <= 4*local_x - 2) and (local_y > 2*local_x):
            if local_y % 2:
                triangle_vertice = [[local_x - 1,2 * local_x - (local_y+3)/2],[local_x - 1,2*local_x - (local_y + 1)/2],[local_x,2*local_x - (local_y + 1)/2]]
            else:
                triangle_vertice = [[local_x,2*local_x - 1 - local_y/2],[local_x,2*local_x - local_y/2],[local_x - 1,2*local_x - 1 - local_y/2]]
        if (local_y <= 6*local_x - 2) and (local_y > 4*local_x - 2):
            if local_y % 2:
                triangle_vertice = [[3*local_x - (local_y + 3)/2,2*local_x - (local_y + 3)/2],[3*local_x - (local_y + 3)/2,2*local_x - (local_y + 1)/2],[3*local_x - (local_y + 1)/2,2*local_x - (local_y + 1)/2]]
            else:
                triangle_vertice = [[3*local_x - 1 - local_y/2,2*local_x - 1 - local_y /2],[3*local_x - 1 - local_y/2,2*local_x - local_y /2],[3*local_x - 2 - local_y/2,2*local_x - 1 - local_y /2]]
        if (local_y <= 8*local_x-4)and (local_y>6*local_x-2):
            if local_y % 2:
                triangle_vertice = [[3*local_x - (local_y+3)/2,-local_x],[3*local_x - (local_y + 3)/2,-local_x + 1],[3*local_x - (local_y + 1)/2,-local_x + 1]]
            else:
                triangle_vertice = [[-local_y/2+3*local_x-1,-local_x],[-local_y/2+3*local_x-1,-local_x+1],[-local_y/2+3*local_x-2,-local_x]]
        if (local_y <= 10*local_x - 4)and(local_y > 8*local_x - 4):
            if local_y % 2:
                triangle_vertice = [[-local_x,-5*local_x+(local_y+3)/2],[-local_x,-5*local_x+(local_y+5)/2],[-local_x+1,-5*local_x+(local_y+5)/2]]
            else:
                triangle_vertice = [[-local_x+1,-5*local_x+local_y/2+2],[-local_x+1,-5*local_x+local_y/2+3],[-local_x,-5*local_x+local_y/2+2]]
        if (local_y <= 12*local_x - 6)and(local_y > 10*local_x - 4):
            if local_y % 2:
                triangle_vertice = [[(local_y+5)/2-6*local_x,-5*local_x+(local_y+3)/2],[(local_y+5)/2-6*local_x,-5*local_x+(local_y+5)/2],[(local_y+7)/2-6*local_x,-5*local_x+(local_y+5)/2]]
            else:
                triangle_vertice = [[local_y/2-6*local_x+3,-5*local_x+local_y/2+2],[local_y/2-6*local_x+3,-5*local_x+local_y/2+3],[local_y/2-6*local_x+2,-5*local_x+local_y/2+2]]
                
        self.triangle_vertice = triangle_vertice
    def copy(self):
        return(Local_Point(self.vertice_A,self.vertice_B,self.vertice_C,self.x,self.y,self.z,self.owner,self.local_x,self.local_y))
    
    def compare_edge_neighbour(self,p2):#比较两个点的位置是否一样
        flag = False
        p1 = self
        symm = ['012','021','102','120','201','210']
        p1 = [p1.vertice_A,p1.vertice_B,p1.vertice_C,p1.x,p1.y,p1.z]
        p2 = [p2.vertice_A,p2.vertice_B,p2.vertice_C,p2.x,p2.y,p2.z]          
        for s in symm:
            temp = []
            for i in range(3):
                temp.append(p2[int(s[i])]) 
            for i in range(3):
                temp.append(p2[int(s[i])+3])
            if temp[0] == p1[0] and temp[1] == p1[1] and temp[2] == p1[2]:
                if (temp[3] == p1[3] and temp[4] == p1[4] and abs(temp[5] - p1[5]) == 1) or (temp[3] == p1[3] and temp[5] == p1[5] and abs(temp[4] - p1[4]) == 1) or (temp[4] == p1[4] and temp[5] == p1[5] and abs(temp[3] - p1[3]) == 1):
                    flag = True
                    
        if N in p1[3:6] and p1[3]+p1[4]+p1[5]==2*N + 1:  #跨三角区域边界
            for s in symm:
                temp = []
                for i in range(3):
                    temp.append(p2[int(s[i])]) 
                for i in range(3):
                    temp.append(p2[int(s[i])+3])
                if (temp[0] == p1[0] and temp[1] == p1[1] and temp[2] != p1[2] and temp[3] == p1[3] and temp[4] == p1[4] and temp[5] == N and p1[5] == N):
                    flag = True
        return flag
                
    def compare_vertex_neighbour(self,p2):
        flag = False
        p1 = self
        symm = ['012','021','102','120','201','210']
        p1 = [p1.vertice_A,p1.vertice_B,p1.vertice_C,p1.x,p1.y,p1.z]
        p2 = [p2.vertice_A,p2.vertice_B,p2.vertice_C,p2.x,p2.y,p2.z]          
        for s in symm:
            temp = []
            for i in range(3):
                temp.append(p2[int(s[i])]) 
            for i in range(3):
                temp.append(p2[int(s[i])+3])
            if temp[0] == p1[0] and temp[1] == p1[1] and temp[2] == p1[2]:
                if abs(temp[3] - p1[3]) <= 1 and abs(temp[4] - p1[4]) <= 1 and abs(temp[5] - p1[5]) <= 1:
                    flag = True
                    
        if N in p1[3:6]:  #跨三角区域边界
            for s in symm:
                temp = []
                for i in range(3):
                    temp.append(p2[int(s[i])]) 
                for i in range(3):
                    temp.append(p2[int(s[i])+3])
                if (temp[0] == p1[0] and temp[1] == p1[1] and temp[2] != p1[2] and abs(temp[3] - p1[3]) <=  1 and abs(temp[4] - p1[4])<= 1 and temp[5] == N and p1[5] == N)or(temp[1] == p1[1] and temp[2] == p1[2] and temp[0] != p1[0] and abs(temp[4] - p1[4]) <=  1 and abs(temp[5] - p1[5])<= 1 and temp[3] == N and p1[3] == N)or(temp[2] == p1[2] and temp[0] == p1[0] and temp[1] != p1[1] and abs(temp[5] - p1[5]) <=  1 and abs(temp[3] - p1[3])<= 1 and temp[4] == N and p1[4] == N):
                    flag = True
                if (temp[0] == p1[0] and temp[3] == 1 and p1[3] == 1 and temp[4] == N and p1[4] == N and temp[5] == N and p1[5] == N):
                    flag = True       
        return flag
       

class lattice():#棋盘
    def __init__(self):#初始化表格
        temp = []
        for face in face_set:
            for i in range(N):
                for j in range(N):
                    for k in range(N):
                        x = i + 1
                        y = j + 1
                        z = k + 1
                        if (x+y+z==2*N+2)or(x+y+z==2*N+1):
                            temp.append(Point(face[0],face[1],face[2],x,y,z,M))
        self.lattice = temp
        temp = []
        for i in range(M):
            temp.append([])
        self.figure = temp
        self.local_chart = []
        
    def get_local_chart(self,n,m=0):#以n为中心，m为重复轴的参数，每个点获得一个局部坐标
        axis = []#六根轴
        temp = get_local_coordinate(n)
        for i in range(5):
            axis.append(temp[(i+m)%5])
        axis.append(axis[0])
        local_chart = []
        for p in self.lattice:#添加常规点
            vertice = [p.vertice_A,p.vertice_B,p.vertice_C]
            attribute = [p.x,p.y,p.z]    
            if n in vertice:
                local_x = attribute[vertice.index(n)]
                for ax in axis:
                    if (ax in vertice) and (axis[axis.index(ax)+1] in vertice):
                        temp_i = axis.index(ax)
                        local_distance_to_lower_bound = attribute[vertice.index(ax)] - attribute[vertice.index(axis[temp_i+1])] + local_x
                        local_y = temp_i * (2 * local_x - 1) + local_distance_to_lower_bound 
                        pp = Local_Point(p.vertice_A,p.vertice_B,p.vertice_C,p.x,p.y,p.z,p.owner,local_x,local_y)
                        local_chart.append(pp)
                        break
        
        for i in range(N):#添加无意义点形成六边形
            for j in range(N):
                for k in range(N):
                    x = i + 1
                    y = j + 1
                    z = k + 1
                    if (x+y+z==2*N+2)or(x+y+z==2*N+1):
                        local_y = z - y + x + 5 * (2 * x - 1)
                        local_chart.append(Local_Point(n,axis[0],axis[0],x,y,z,M + 1,x,local_y))
                          
        self.local_chart = local_chart
        return local_chart
            
                
    def save(self,path='condition.xls'):#保存进度
        workbook = xlwt.Workbook(encoding = 'utf-8')
        worksheet = workbook.add_sheet('Worksheet')
        k=0
        for p in self.lattice:
            worksheet.write(k,0, label = p.vertice_A)
            worksheet.write(k,1, label = p.vertice_B)
            worksheet.write(k,2, label = p.vertice_C)
            worksheet.write(k,3, label = p.x)
            worksheet.write(k,4, label = p.y)
            worksheet.write(k,5, label = p.z)
            worksheet.write(k,6, label = p.owner)
            k= k + 1
        workbook.save(path)
        
    def save_figure(self,path='condition.xls'):#保存进度
        workbook = xlwt.Workbook(encoding = 'utf-8')
        worksheet = workbook.add_sheet('Figure')
        for k in range(M):
            col = 0
            for f in self.figure[k]:
                worksheet.write(k,col, label = f)
                col = col + 1
        workbook.save(path)
                
    def new_load(self,path='condition.xls'):#读取进度
        workbook = xlrd.open_workbook(path)
        for sheet in workbook.sheets():
            if sheet.name == 'Worksheet':
                self.lattice = []
                for i in range(sheet.nrows):
                    temp = Point(sheet.cell_value(i,0),sheet.cell_value(i,1),sheet.cell_value(i,2),sheet.cell_value(i,3),sheet.cell_value(i,4),sheet.cell_value(i,5),sheet.cell_value(i,6))
                    self.lattice.append(temp)
    
    def load(self,path='condition.xls'):#读取进度
        workbook = xlrd.open_workbook(path)
        for sheet in workbook.sheets():
            if sheet.name == 'Worksheet':
                N = len(self.lattice)
                t = -1
                for i in range(sheet.nrows):
                    temp = Point(sheet.cell_value(i,0),sheet.cell_value(i,1),sheet.cell_value(i,2),sheet.cell_value(i,3),sheet.cell_value(i,4),sheet.cell_value(i,5),sheet.cell_value(i,6))
                    delta = 0
                    if temp.valid():
                        flag = True
                        while flag:
                            t = t + 1
                            delta = delta + 1
                            if self.lattice[t % N].point_compare_position(temp):
                                self.lattice[t % N] = temp
                                flag = False
                            if delta >= N:
                                flag = False
    
    def load_figure(self,path='condition.xls',mode = 0):#读取未存量形状表
        if mode:#重新加载所有图形
            temp = []
            for i in range(M):
                temp.append([])
            self.figure = temp
        workbook = xlrd.open_workbook(path)
        for sheet in workbook.sheets():
            if sheet.name == 'Figure':
                for k in range(sheet.nrows):
                    for t in range(len(sheet.row(k))):
                        if sheet.cell_value(k,t)<>'':
                            self.figure[k].append(str(sheet.cell_value(k,t)))
                            
    def figure_bonus(self,path='condition.xls'):
        global global_file_name
        workbook = xlrd.open_workbook(path)
        for sheet in workbook.sheets():
            if sheet.name == 'Bonus':
                for k in range(sheet.nrows):
                    for t in range(len(sheet.row(k))):
                        temp = int(sheet.cell_value(k,t))
                        if sheet.cell_value(k,t) in [1,2,3,4,5,6]:
                            self.generate_figure(temp,k)
        self.save_figure(global_file_name+'_figure.xls')
        workbook = xlwt.Workbook(encoding = 'utf-8')
        workbook.add_sheet('Bonus')
        workbook.save(path)
                
                
                
    def lattice_score(self):#算分
        score = [0] * (M+1)
        for p in self.lattice:
            score[p.owner] = score[p.owner] + 1
        
        return score
    def generate_figure(self,n,player,mode = 0,st = ''):
        if st[:5] == "00111":#生成形状时的一个例外！此情形会往回走一步
            st = "111111"
        if mode == 0:
            z = list(numpy.random.randint(2,size=n))
            z = [str(j) for j in z]
            st = ''.join(z)
            self.figure[player].append(st)
        if mode == 1:
            self.figure[player].append(st)
    

    def deviate_figure(self,player,figure_num):
        pass
    def move_figure_point(self,point,direction):
        delta_x = 0
        delta_y = 0
        if direction == 'w':
            delta_x = 1
            delta_y = 0
        if direction == 'e':
            delta_x = 1
            delta_y = 1
        if direction == 'd':
            delta_x = 0
            delta_y = 1
        if direction == 'x':
            delta_x = -1
            delta_y = 0
        if direction == 'z':
            delta_x = -1
            delta_y = -1
        if direction == 'a':
            delta_x = 0
            delta_y = -1
        temp_triangle_vertice = [[point[0][0]+delta_x,point[0][1]+delta_y],[point[1][0]+delta_x,point[1][1]+delta_y],[point[2][0]+delta_x,point[2][1]+delta_y]]
        for pt in temp_triangle_vertice:
            if abs(pt[0])>N or abs(pt[1])>N or abs(pt[0]-pt[1])>N:#不要移出六边形边框
                return False#没找到的话返回一个无效值
        return temp_triangle_vertice
        
    def search_point(self,point):
        temp_triangle_vertice = point
        t = 0#游动指标，在上一个点附近找下一个点
        delta = 0
        cycle = len(self.local_chart)
        while delta < cycle:
            pt = self.local_chart[t]
            pt = pt.copy()
            if (pt.triangle_vertice[0] == temp_triangle_vertice[0]) and (pt.triangle_vertice[1] == temp_triangle_vertice[1]) and (pt.triangle_vertice[2] == temp_triangle_vertice[2]):
                return pt
            delta = delta + 1
            t = (t+1) % cycle
        return False#没找到的话返回一个无效值    
    
    def put_figure(self,player,figure_num,figure_points):
        temp_figure_points = []
        for point in figure_points:
            pt = la.search_point(point)
            if pt:
                temp_figure_points.append(pt)
            else:
                return False
        figure_points = temp_figure_points            
        legal = self.activate(figure_points,player)#是否符合放置规则    
        flag = False
        if legal and len(self.figure[player][figure_num]) == len(figure_points):#且符合图形没有少点            
            for pt in figure_points:#最后多一位冗余，第一格其实是固定的
                t = 0#游动指标，在上一个点附近找下一个点
                delta = 0
                cycle = len(self.local_chart)
                while delta < cycle:
                    point = self.local_chart[t]
                    if (point.local_x == pt.local_x) and (point.local_y == pt.local_y):
                        self.local_chart[t].owner = player#占据！
                        #print player,figure_num,self.figure[player][figure_num],len(figure_points)
                        break
                    delta = delta + 1
                    t = (t+1) % cycle   
            for pt in figure_points:#最后多一位冗余，第一格其实是固定的            
                t = 0#游动指标，在上一个点附近找下一个点
                delta = 0
                cycle = len(self.lattice)
                while delta < cycle:
                    point = self.lattice[t]
                    if point.point_compare_position(pt):
                        self.lattice[t].owner = player#占据！
                        #print player,figure_num,self.figure[player][figure_num],len(figure_points)
                        break
                    delta = delta + 1
                    t = (t+1) % cycle 
            del self.figure[player][figure_num]
            flag = True
            print self.lattice_score()
        return flag
                    
        
    def get_figure(self,player,figure_num,core_x = 1,core_y = 1):#获得图形的局部坐标
        temp_x = core_x#core_x是中心格的局部坐标，temp_x是生成格的局部坐标
        temp_y = core_y
        temp_figure = []
        flag = 1#格的奇偶性
        direction = 1#下一步横向移动的方向
        for step in self.figure[player][figure_num]:#最后多一位冗余，第一格其实是固定的
            t = 0#游动指标，在上一个点附近找下一个点
            delta = 0
            cycle = len(self.local_chart)
            while delta < cycle:
                point = self.local_chart[t]
                if (point.local_x == temp_x) and (point.local_y == temp_y):
                    point = point.copy()
                    temp_figure.append(point.triangle_vertice)
                    if flag:
                        if step == '0':
                            temp_y = temp_y + (temp_y-1) / (temp_x * 2 -1) * 2 + 1
                            temp_x = temp_x + 1 
                            direction = 1
                        else:
                            temp_y = temp_y + direction
                    if not flag:
                        if step == '0':
                            temp_y = temp_y + 1
                            direction = 1
                        else:
                            temp_y = temp_y - 1
                            direction = - 1
                    temp_y = (temp_y - 1) % ((temp_x * 2 - 1)*6) + 1
                    flag = ((temp_y - 1) % (temp_x * 2 -1) + 1) % 2
                    break
                delta = delta + 1
                t = (t+1) % cycle
                
        return temp_figure


    def activate(self,figure_points,player):
        flag = False
        for point in figure_points:#顶点有邻
            for pt in self.lattice:
                if point.compare_vertex_neighbour(pt):
                    if player == pt.owner:
                        flag = True
            
        if self.lattice_score()[player] == 0:#还没开张过顶点不用邻
            flag = True

        for point in figure_points:            
            for pt in self.lattice:
                if point.compare_edge_neighbour(pt):
                    if player == pt.owner:
                        flag = False
                    
        for point in figure_points:#未被占据
            for pt in self.local_chart:
                if point.point_compare_position(pt):
                    if pt.owner != M:
                        flag = False


           
        return flag        
              

      
    def show_figure(self):
        global global_figure_points
        if len(global_figure_points) != 0:    
            for tr in global_figure_points:
                tr_vertice = []
                for pt in tr:
                    pt_coordinate = pt[0] * v1 + pt[1] * v2 + mid_point
                    tr_vertice.append(pt_coordinate[0])
                    tr_vertice.append(pt_coordinate[1])
                my_canvas.create_polygon(tr_vertice,fill='black',outline='black',stipple="gray50")
                
            
    def show_local_chart(self, renew_part = []):
        global global_player
        global my_canvas              
        v1=numpy.array([-1,-1.732])*d
        v2=numpy.array([2,0])*d
        if renew_part:              
            for tr in self.local_chart:
                if tr.triangle_vertice in renew_part:
                    tr_vertice = []
                    for pt in tr.triangle_vertice:
                        pt_coordinate = pt[0] * v1 + pt[1] * v2 + mid_point
                        tr_vertice.append(pt_coordinate[0])
                        tr_vertice.append(pt_coordinate[1])
                    if tr.owner == global_player:
                        my_canvas.create_polygon(tr_vertice,fill='red',outline='black',stipple="gray50")
                    if tr.owner != global_player and tr.owner in gamers:
                        my_canvas.create_polygon(tr_vertice,fill='blue',outline='black',stipple="gray50")
                    if tr.owner == M:
                        my_canvas.create_polygon(tr_vertice,fill='white',outline='black')
                    if tr.owner == M+1:
                        my_canvas.create_polygon(tr_vertice,fill='black',outline='black')
        else:            
            for tr in self.local_chart:
                tr_vertice = []
                for pt in tr.triangle_vertice:
                    pt_coordinate = pt[0] * v1 + pt[1] * v2 + mid_point
                    tr_vertice.append(pt_coordinate[0])
                    tr_vertice.append(pt_coordinate[1])
                if tr.owner == global_player:
                    my_canvas.create_polygon(tr_vertice,fill='red',outline='black',stipple="gray50")
                if tr.owner != global_player and tr.owner in gamers:
                    my_canvas.create_polygon(tr_vertice,fill='blue',outline='black',stipple="gray50")
                if tr.owner == M:
                    my_canvas.create_polygon(tr_vertice,fill='white',outline='black')
                if tr.owner == M+1:
                    my_canvas.create_polygon(tr_vertice,fill='black',outline='black')
    def show_axis(self):    
        global a0,a1,a2,a3,a4,a5,a6        
        axis = []#六根轴
        temp = get_local_coordinate(global_chart)
        for i in range(5):
            axis.append(temp[(i+global_axis)%5])
        axis.append(axis[0])
        a0 = my_canvas.create_text(mid_point[0],mid_point[1],text=global_chart)
        a1 = my_canvas.create_text(mid_point[0]+v2[0]*(N+1),mid_point[1]+v2[1]*(N+1),text=axis[0])
        a2 = my_canvas.create_text(mid_point[0]+v1[0]*(N+1)+v2[0]*(N+1),mid_point[1]+v1[1]*(N+1)+v2[1]*(N+1),text=axis[1])
        a3 = my_canvas.create_text(mid_point[0]+v1[0]*(N+1),mid_point[1]+v1[1]*(N+1),text=axis[2])        
        a4 = my_canvas.create_text(mid_point[0]-v2[0]*(N+1),mid_point[1]-v2[1]*(N+1),text=axis[3])
        a5 = my_canvas.create_text(mid_point[0]-v1[0]*(N+1)-v2[0]*(N+1),mid_point[1]-v1[1]*(N+1)-v2[1]*(N+1),text=axis[4])  
        a6 = my_canvas.create_text(mid_point[0]-v1[0]*(N+1),mid_point[1]-v1[1]*(N+1),text=axis[5])                                             

    def delete_axis(self):
        global a0,a1,a2,a3,a4,a5,a6  
        my_canvas.delete(a0)
        my_canvas.delete(a1)
        my_canvas.delete(a2)
        my_canvas.delete(a3)
        my_canvas.delete(a4)
        my_canvas.delete(a5)
        my_canvas.delete(a6)   

            
    
"""
主程序
"""



la = lattice()

global_player = 0

global_axis = -1#当前局部坐标系

global_fig_num = -1

global_figure_points = []

global_chart = 12

v1=numpy.array([-1,-1.732])*d_unit

v2=numpy.array([2,0])*d_unit
              
mid_point=numpy.array([400,300])               

root = Tk()

root.title('temp')
#root.iconbitmap('d:/Users/Admin/Desktop/chess/temp.ico')
root.geometry("1200x1200")

def file_selection():
    global global_file_name
    global la
    global_file_name = lb3.get(lb3.curselection())
    la.new_load(global_file_name + '.xls')
    la.load_figure(global_file_name + '_figure.xls',1)
    
    #la.load_figure(global_file_name + '_figure.xls')    
    
 
def figure_bonus():
    global global_file_name
    la.figure_bonus(global_file_name+'_weekly_bonus.xls')    
    
def player_selection():
    global global_player
    global global_figure_points
    global global_fig_num
    global_player = lb1.get(lb1.curselection())
    global_figure_points = []
    if la.figure[global_player]:
        global_fig_num = (global_fig_num + 1) % len(la.figure[global_player])
        global_figure_points = la.get_figure(global_player,global_fig_num) 

    #print global_player,global_fig_num
    la.show_local_chart()
    la.show_figure()
    
def chart_selection():
    global global_axis
    global la
    global global_chart
    global a0,a1,a2,a3,a4,a5,a6
    my_canvas.delete("all")
    global_axis = (global_axis + 1) % 5 #切换坐标轴顺序    
    global_chart = lb2.get(lb2.curselection())
    la.get_local_chart(global_chart,global_axis)
    #print temp_chart,global_axis
    la.show_local_chart()
    la.show_axis()
    
def move_put(event):
    global global_player
    global global_figure_points
    global global_fig_num
    global global_chart
    global global_axis
    global a0,a1,a2,a3,a4,a5,a6
    global my_canvas
    if event.char in ['w','e','d','x','z','a']:
        direction = event.char
        temp_figure_points = []
        for point in global_figure_points:
            pt = la.move_figure_point(point,direction)
            if pt:
                temp_figure_points.append(pt)
            else:
                temp_figure_points = global_figure_points
                break
        la.show_local_chart(global_figure_points)
        global_figure_points = temp_figure_points
        la.show_figure()
   
    if event.char == 'p':
        if len(la.figure[global_player])>global_fig_num:
            temp_figure_points = global_figure_points
            flag = la.put_figure(global_player,global_fig_num,global_figure_points)
            if flag:
                global_figure_points = []
                my_canvas.delete("all")
                la.show_local_chart()
                la.show_axis()
                la.save(global_file_name + '.xls')
                la.save_figure(global_file_name + '_figure.xls')
            else:
                global_figure_points = temp_figure_points
                la.show_local_chart(temp_figure_points)
                la.show_figure()

    
    if event.char == 's':
        my_canvas.delete("all")
        global_axis = (global_axis + 1) % 5 #切换坐标轴顺序    
        la.get_local_chart(global_chart,global_axis)
        la.show_local_chart()
        la.show_figure()
        la.show_axis()
#当前玩家   
B1 = Button(root, text ="player",width = 5,height = 2, command = player_selection)
B1.pack(side='right')
player_list1 = IntVar()
player_list1.set((0,1,2,3,4,5,6,7,8,9,10,11,12))
lb1 = Listbox(root,listvariable=player_list1,width = 4) 
lb1.pack(side='right')

#当前局部坐标系
B2 = Button(root, text ="chart",width = 5,height = 2, command = chart_selection)
B2.pack(side='right')
player_list2 = IntVar()
player_list2.set((0,1,2,3,4,5,6,7,8,9,10,11))
lb2 = Listbox(root,listvariable=player_list2,width = 4) 
lb2.pack(side='right')

#当前表个名
B3 = Button(root, text ="file",width = 5,height = 2, command = file_selection)
B3.pack(side='right')
player_list3 = IntVar()
player_list3.set(("202403","202404"))
lb3 = Listbox(root,listvariable=player_list3,width = 8) 
lb3.pack(side='right')

B4 = Button(root, text ="Bonus",width = 5,height = 2, command = figure_bonus)
B4.pack()


root.bind("<Key>",move_put)

my_canvas = Canvas(root,width=800,height=800,bg='white')

my_canvas.pack(side='left', expand='no', anchor='center', fill='y', padx=5, pady=5)



root.mainloop()
