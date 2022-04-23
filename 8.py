import pygame as pg
import numpy as np
from math import sqrt


class Node:
    def __init__(self, data, level, f_score, parent, direct):
        self.data = data
        self.n = sqrt(len(data))
        if parent == None:
            self.level = 1
        else:
            self.level = level * 2
        self.f_score = f_score
        self.parent = parent
        self.thisdirect = direct
    def find_index(self, num):
        index = self.data.index(num)
        i = index // self.n
        j = index - (i * self.n)
        return i, j
    def possible_moves(self):
        i, j = self.find_index("2")
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        directions_name = ["Up", "Down", "Left", "Right"]
        all_directions = {directions[i]:directions_name[i] for i in range(4)}
        
        possible_moves = []
        for k in directions:
            if not ((i+k[0]<0) or (i+k[0]>self.n-1) or (j+k[1]<0) or (j+k[1]>self.n-1)):
                possible_moves.append((all_directions[k]))
        left =  int(((i*self.n)+j)-1)
        right = int(((i*self.n)+j)+1)
        top = int(((i-1)*self.n)+j)
        bottom = int(((i+1)*self.n)+j)
        for i in possible_moves:
            if i=="Up":
                if top<0 or self.data[top]=="1":
                    possible_moves.remove("Up")
            elif i=="Down":
                if (bottom>=self.n**2) or (self.data[bottom]=="1"):
                    possible_moves.remove("Down")
            elif i=="Left":
                if left<0 or self.data[left]=="1":
                    possible_moves.remove("Left")
            else:
                if (right>=self.n**2) or (self.data[right]=="1"):
                    possible_moves.remove("Right")
        index = self.data.find("2")
        if "Left" in possible_moves and index%self.n==0:
            possible_moves.remove("Left")
        elif "Right" in possible_moves and (index+1)%self.n==0:
            possible_moves.remove("Right")
        
        return possible_moves
    def generate_children(self):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        directions_name = ["Up", "Down", "Left", "Right"]
        all_directions = {directions_name[i]:directions[i] for i in range(4)}
        
        possible_directions = self.possible_moves()
        
        i,j = self.find_index("2")
        
        left =  int(((i*self.n)+j)-1)
        right = int(((i*self.n)+j)+1)
        top = int(((i-1)*self.n)+j)
        bottom = int(((i+1)*self.n)+j)
        
            
        children = []
        for p in possible_directions:
            puzzle_list = list(self.data)
            zero_index = puzzle_list.index("2")
            if p == "Up":
                if puzzle_list[top]!="4":
                    puzzle_list[zero_index], puzzle_list[top]= "1", "2"
                    di = "Up"
                else:
                    continue
            elif p=="Down":
                if puzzle_list[bottom]!="4":
                    puzzle_list[zero_index], puzzle_list[bottom]= "1", "2"
                    di = "Down"
                else:
                    continue
            elif p=="Right":
                if puzzle_list[right]!="4":
                    puzzle_list[zero_index], puzzle_list[right]= "1", "2"
                    di = "Right"
                else:
                    continue
            elif p=="Left":
                if puzzle_list[left]!="4":
                    puzzle_list[zero_index], puzzle_list[left]= "1", "2"
                    di = "Left"
                else:
                    continue
            children.append(("".join(puzzle_list),di))
            
        children_obj = []
        for i in children:
            children_obj.append(Node(i[0],self.level+1,0,self,i[1]))
        return children_obj


class Puzzle:
    def __init__(self, current, goal):
        self.puzzle = current
        self.open = []
        self.closed = []
        self.visited = {}
        self.goal = goal
        
    def find_index(self, cur, num):
        index = cur.find(num)
        i = index // (sqrt(len(cur)))
        j = index - (i * (sqrt(len(cur))))
        return i, j 
    def f_score(self, current, goal):
        return self.h_score(current.data, goal) + current.level
    def h_score(self, current, goal):
        total = 0
        i,j= self.find_index(current, str(2))
        x,y= self.find_index(goal, str(2))
        total+= abs(i-x) + abs(j-y)
        return total
    def process(self):
        start = Node(self.puzzle, 0, 0, None,None)
        
        self.open.append(start)
        
        while True:
            cur = self.open[0]
            if (cur.data[self.goal.find("2")]=="2"):
                _list = []
                _list.append(cur)
                while cur.parent != None:
                    _list.append(cur.parent)
                    cur = cur.parent
                else:
                    _list.append(cur.parent)
                _list = _list[::-1]
                """t = 0
                for i in _list:
                    if i!=None:
                        length_list = int(sqrt(len(i.data)))
                        for q in range(0,len(i.data),length_list):
                            for w in range(length_list):
                                print(i.data[q+w],end=" ")
                            print()
                        print(i.thisdirect)
                        print("********************")
                    t+=1
                print("Total-steps:",t-2)"""
                return _list
                break
            for i in cur.generate_children():
                i.fval = self.f_score(i,self.goal)
                if i.data not in self.visited or self.visited[i.data]>i.fval:
                    self.open.append(i)
                    self.visited[i.data]=i.fval
            self.closed.append(cur)
            self.visited[cur.data]=self.h_score(cur.data,self.goal)
            del self.open[0]
            
            self.open.sort(key = lambda x:x.fval, reverse=False)


import pygame as pg
pg.init()

print("Hello, and welcome to Maze solver!")
n = 20

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 166, 147)
red = (122, 0, 0)

width = n * 10 - 10
height = n * 10 + 50

gameDisplay = pg.display.set_mode((width, height))
pg.display.set_caption("Maze")

x = 0
y = 0
for i in range((n*n)):
    exec(f"""sq{i} = pg.draw.rect(gameDisplay,white,({x},{y},10,10),1)""")
    exec(f"sq{i}_x, sq{i}_y = {x},{y}")
    x+=10
    if x>=n*10:
        x=0
        y+=10

start_key = pg.draw.rect(gameDisplay,white,(30,n*10+10,60,30),2)
        
def clicker(x,y,logic_board,point):
    pg.draw.line(gameDisplay, (255,0,0),(x,y),(x + 10,y + 10),1)
    pg.draw.line(gameDisplay, (255,0,0),(x,y + 10),(x + 10, y),1)
    logic_board[point//n][point%n]="4"
    return logic_board

game_logic_board = []
for i in range(0,n*n,n):
    row = []
    for j in range(n):
        row.append("0")
    game_logic_board.append(row)
game = True
while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
        if event.type == pg.MOUSEBUTTONUP:
            click_pos = pg.mouse.get_pos()
            if start_key.collidepoint(click_pos):
                game = False
            for i in range(0,n*n):
                exec(f"""if sq{i}.collidepoint(click_pos):
   game_logic_board = clicker(sq{i}_x,sq{i}_y,game_logic_board,{i})""")
            x = ""
            for t in range(len(game_logic_board)):
                for y in range(len(game_logic_board)):
                    x+=str(game_logic_board[t][y])
    pg.display.update()
pg.quit()


import pygame as pg
pg.init()
goal = ["0" for i in range(n*n)]
goal[(n*n)-1]="2"
goal = "".join(goal)
x = list(x)
x[0]="2"
x = "".join(x)
x = Puzzle(x,goal)
solution = x.process()

width = n * 10
height = n * 10

gameDisplay = pg.display.set_mode((width, height))
pg.display.set_caption("solution")

x = 0
y = 0
for row in game_logic_board:
    x=0
    for cell in row:
        if cell=="0":
            pg.draw.rect(gameDisplay,black,(x,y,10,10),1)
        elif cell=="1":
            pg.draw.rect(gameDisplay,green,(x,y,10,10),0)
        elif cell=="2":
            pg.draw.rect(gameDisplay,red,(x,y,10,10),0)
        elif cell=="4":
            pg.draw.rect(gameDisplay,white,(x,y,10,10),1)
        x+=10
    y+=10
            
game = True
while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
    pg.display.update()
pg.quit()