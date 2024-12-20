import numpy as np 
import scipy.sparse as sp
from dataclasses import dataclass
from typing import List
from tqdm import tqdm

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
        return self.x >= 0 and self.x < grid[0] and self.y >= 0 and self.y < grid[1]


with open("inputs/day20.txt") as f:
    arr = np.array([list(l.strip()) for l in f])

X,Y = np.meshgrid(np.arange(0,arr.shape[1]),np.arange(0,arr.shape[0]))

smask = arr == 'S'
start = Point(X[smask][0],Y[smask][0])
emask = arr == 'E'
end = Point(X[emask][0],Y[emask][0])
pmask = arr == '.'
pts = set([Point(x,y) for (x,y) in zip(X[pmask],Y[pmask])])
pts.add(start)
pts.add(end)
wmask = arr == '#'
walls = set([Point(x,y) for (x,y) in zip(X[wmask],Y[wmask])])

back_scatter = {}
for (i,p) in enumerate(pts):
    back_scatter[p] = i

m = sp.lil_matrix((len(pts),len(pts)),dtype=int)
for p in pts:
    up = p.up()
    down = p.down()
    left = p.left()
    right = p.right()
    for next in [up,down,left,right]:
        if next in back_scatter and next not in walls:
            m[back_scatter[p],back_scatter[next]] = 1


print("sparse constructed")

seg1_dist = sp.csgraph.dijkstra(m,indices=back_scatter[start],directed=True,min_only=True)
seg2_dist = sp.csgraph.dijkstra(m,indices=back_scatter[end],directed=True,min_only=True)
base_time = seg1_dist[back_scatter[end]]

single_skip = 0
long_skip = 0

for p1 in tqdm(pts):
    init_path = seg1_dist[back_scatter[p1]]
    for dx in range(-20,21):
        for dy in range(-20,21):
            cheat_length = abs(dx) + abs(dy)
            if cheat_length > 20:
                continue

            p2 = Point(p1.x+dx,p1.y+dy) 
            if p1 == p2:
                continue

            if p2 not in back_scatter:
                continue
            
            tail_path = seg2_dist[back_scatter[p2]]
            curr_path = init_path+tail_path+cheat_length

            if base_time - curr_path < 100:
                continue

            if cheat_length <= 20:
                long_skip += 1

            if cheat_length <= 2:
                single_skip += 1
        
print(single_skip)
print(long_skip)
            

        


#print(cheat_delta)
#print(count)