import numpy as np 
from tqdm import tqdm

with open("inputs/day6.txt") as f:
    arr = np.array([ [ c for c in l.strip()] for l in f],dtype=str)

[X,Y] = np.meshgrid(np.arange(arr.shape[0]),np.arange(arr.shape[1]))
x_start = X[arr=="^"][0]
y_start = Y[arr=="^"][0]

x_blocks = X[arr=="#"]
y_blocks = Y[arr=="#"]

block_locs = list(zip(x_blocks,y_blocks))

start = (x_start,y_start)

dirs = {"U":(0,-1),"D":(0,1),"L":(-1,0),"R":(1,0)}
dirs_order = "URDL"

class Maze: 
    def __init__(self, block_locations,shape,start_loc,start_dir=0):
        self.block_locations = set(block_locations)
        self.shape = shape
        self.start = start_loc
        self.start_dir = start_dir
        self.graph = {}
        self.build_graph()

    def isoutside(self,pos):
        return pos[0] < 0 or pos[0] >= self.shape[0] or pos[1] < 0 or pos[1] >= self.shape[1]

    def build_graph(self):
        nodes = set()
        for pos in self.block_locations:
            for (i,dir) in enumerate(dirs_order):
                input_dir = (i+2)%4
                output_dir = (i+3)%4    
                (xc,yc) = pos
                (xd,yd) = dirs[dir]
                (xp, yp) = (xc + xd, yc + yd)
                node_pos = (xp,yp)
                if node_pos in self.block_locations:
                    continue

                self.graph[(node_pos,input_dir)] = ((node_pos,output_dir),True)
                nodes.add((node_pos,output_dir))

        for node in nodes:
            (pos,dir) = node
            if node in self.graph:
                continue
            next_node = self.get_next_node(pos,dir)
            if next_node is not None:
                self.graph[node] = next_node




    def get_next_node(self,pos,dir):
        (xd,yd) = dirs[dirs_order[dir]]
        current_pos = pos 
        for _ in range(0,max(arr.shape)+1):
            (xc,yc) = current_pos
            new_pos = (xc + xd,yc + yd)
            if self.isoutside(new_pos) :
                return ((new_pos,dir),False)

            if new_pos in self.block_locations and current_pos != pos:
                return ((current_pos,dir),True)
            
            current_pos = new_pos
        
        return None
            
    def run(self,function = lambda x,y,z: None):
        (next_pt,cont) = self.get_next_node(self.start,self.start_dir)
        function(self,(self.start,self.start_dir),next_pt)
        seen = set()
        seen.add(next_pt)
        while cont:
            curr_pt = next_pt
            next_pt,cont = self.graph[curr_pt]
            function(self,curr_pt,next_pt)
            if next_pt in seen:
                return True
            seen.add(next_pt)

        return False 

    def blocks(self,curr,next):
        (curr_pos,curr_dir) = curr
        (next_pos,next_dir) = next
        (xd,yd) = dirs[dirs_order[curr_dir]]
        (xp,yp) = curr_pos
        for n in range(0,max(arr.shape)+1):
            new_pos = (xp + n*xd,yp + n*yd)
            if new_pos == next_pos or self.isoutside(new_pos):
                break
            yield new_pos

def per_block(fnc):
    def wrapper(self : Maze,curr,next):
        for b in self.blocks(curr,next):
            fnc(self,b)
    return wrapper


m = Maze(block_locs,arr.shape,start)

path = []
visited = set() 

@per_block
def get_path(s,block):
    visited.add(block)
    path.append(block)

m.run(get_path)
print(len(visited))

count = 0
for v in tqdm(list(visited)):
    if visited == start: 
        continue

    m = Maze(block_locs+[v],arr.shape,start)
    if m.run():
        count += 1
print(count)







