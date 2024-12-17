import numpy as np 
from dataclasses import dataclass
from typing import List

with open('inputs/day15.txt') as f:
    arr = []
    for l in f:
        if l.strip() == "":
            break
        arr.append([c for c in l.strip()])
    arr = np.array(arr,dtype=str)
    moves = ""
    for l in f:
        moves += l.strip()

@dataclass(frozen=True)
class Point():
    x : int
    y : int

    def double(self):
        return Point(2*self.x,self.y)
    
    def right(self):
        return Point(self.x+1,self.y)

    def left(self):
        return Point(self.x-1,self.y)

    def up(self):
        return Point(self.x,self.y-1)

    def down(self):
        return Point(self.x,self.y+1)
    
    def move(self,d):
        if d == "<":
            return self.left()
        if d == ">":
            return self.right()
        if d == "^":
            return self.up()
        if d == "v":
            return self.down()
    
    def within(self,grid):
        return self.x >= 0 and self.x < grid.shape[1] and self.y >= 0 and self.y < grid.shape[0]


class Grid(): 
    boxes :set[Point] = set()
    walls : set[Point] = set()
    box_links: dict[Point,List[Point]] = {}
    bot : Point = None

    def __init__(self,arr=None):
        if arr is None:
            return
        
        X,Y = np.meshgrid(np.arange(arr.shape[1]),np.arange(arr.shape[0]))

        wall_x = X[arr == "#"]
        wall_y = Y[arr == "#"]
        bot_x = X[arr == "@"]
        bot_y = Y[arr == "@"]
        box_x = X[arr == "O"]
        box_y = Y[arr == "O"]

        self.walls = set([Point(x,y) for (x,y) in zip(wall_x,wall_y)])
        self.boxes = set([Point(x,y) for (x,y) in zip(box_x,box_y)])
        self.bot = Point(bot_x[0],bot_y[0])
        self.box_links = {}
    
    def copy(self):
        g = Grid()
        g.walls = self.walls.copy()
        g.boxes = self.boxes.copy()
        g.bot = self.bot
        g.box_links = {k:v.copy() for k,v in self.box_links.items()}
        return g
    
    def double_grid(self):
        self.walls = set(sum([[p.double(),p.double().right()] for p in self.walls],[]))
        tmp_boxes = set()
        for b in self.boxes:
            bd = b.double()
            tmp_boxes.add(bd)
            self.box_links[bd] = [bd.right()]
            self.box_links[bd.right()] = [bd]
        self.boxes = tmp_boxes
        self.bot = self.bot.double()

    def print_grid(self):
        grd = np.zeros((max([p.y for p in self.walls])+1,max([p.x for p in self.walls])+1),dtype=str)
        grd[:,:] = "."
        for p in self.walls:
            grd[p.y,p.x] = "#"
        for p in self.boxes:
            grd[p.y,p.x] = "O"
        grd[self.bot.y,self.bot.x] = "@"
        for p in self.box_links:
            if p in self.boxes:
                grd[p.y,p.x] = "["
            else: 
                grd[p.y,p.x] = "]"
        return grd


    def execute_move(self,move: str) -> bool:
        next_pt = self.bot.move(move)
            
        move_set = set()
        r = self.push(next_pt,move,move_set)
        if not r:
            return False
            
        self.update_boxes(move_set,move)
        self.bot = next_pt
        return True
    
    def execute_all_moves(self,moves:str):
        for m in moves:
            self.execute_move(m)    

    
    def push(self,loc:Point,move:str,moved_set : set[Point] = set()):
        if loc in moved_set:
            return True
        
        

        if loc in self.walls:
            return False
    
        if loc not in self.boxes and loc not in self.box_links:
            return True
        
        moved_set.add(loc)

        next_pt = loc.move(move)
        if not self.push(next_pt,move,moved_set):
            return False
        
        if loc in self.box_links:
            for c in self.box_links[loc]:
                if not self.push(c,move,moved_set):
                    return False
            
        return True
    
    def update_boxes(self,moved_set:set[Point],move:str):
        
        new_boxes = set()
        link_updates = {}
        for m in moved_set:
            if m in self.boxes:
                new_boxes.add(m.move(move))

            if m in self.box_links:
                link_updates[m.move(move)] = list([n.move(move) for n in self.box_links[m]])
                del self.box_links[m]

        self.boxes = self.boxes.difference(moved_set)
        self.boxes = self.boxes.union(new_boxes)
        for k,v in link_updates.items():
            self.box_links[k] = v

    def compute_gps(self):
        return sum([100*m.y + m.x for m in self.boxes])

g = Grid(arr) 
g2 = g.copy()
g.execute_all_moves(moves)
print(g.compute_gps())

g2.double_grid()
g2.execute_all_moves(moves)
print(g2.compute_gps())
        






