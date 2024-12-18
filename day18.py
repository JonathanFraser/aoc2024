import numpy as np
import scipy.sparse as sp
import re

falling = []
dm = re.compile(r"(\d+),(\d+)")

with open('inputs/day18.txt') as f:
    for l  in f:
        m = dm.match(l)
        falling.append((int(m.group(1)),int(m.group(2))))



class Maze():
    def __init__(self,size=(71,71)):
        self.all_pts = []
        self.size = size
        self.back_scatter = {}
        for x in range(0,size[0]):
            for y in range(0,size[1]):
                self.back_scatter[(x,y)] = len(self.all_pts)
                self.all_pts.append((x,y))

    def prep_mat(self,blocks):
        self.lm = sp.lil_matrix((self.size[0]*self.size[1],self.size[0]*self.size[1]),dtype=int)
        for a in self.all_pts: 
            if a in blocks:
                continue
            (x,y) = a 
            up = (x,y-1)
            down = (x,y+1)
            left = (x-1,y)
            right = (x+1,y)
            for next in [up,down,left,right]:
                if next in self.back_scatter and next not in blocks:
                    self.lm[self.back_scatter[a],self.back_scatter[next]] = 1

    def compute_min_path(self):
        source = self.back_scatter[(0,0)]
        (xm,ym) = self.size
        end = self.back_scatter[(xm-1,ym-1)]
        (dist,pred,sources) = sp.csgraph.dijkstra(self.lm,indices=source,return_predecessors=True,directed=True,min_only=True)
        mindist = dist[end]
        if mindist == np.inf:
            return None 
        return int(mindist)

maze = Maze()
fall_set = set(falling[:1024])
maze.prep_mat(fall_set)
print(maze.compute_min_path())

start = 0
end = len(falling)
n=0
while end > start+1:
    mid = (start+end) // 2 
    maze.prep_mat(set(falling[:mid]))
    if maze.compute_min_path() is not None:
        start = mid
    else:
        end = mid
    n+=1

for m in range(start-1,end+1):
    maze.prep_mat(set(falling[:m]))
    if maze.compute_min_path() is None:
        break

(fx,fy) = falling[m-1]
print(f"{fx},{fy}")