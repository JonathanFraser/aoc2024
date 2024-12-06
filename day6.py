import numpy as np
from tqdm import tqdm

class Map:
    def __init__(self,arr):
        self.arr = arr
        self.shape = arr.shape
        self.direction = np.array([-1,0])
        X,Y = np.meshgrid(np.arange(self.arr.shape[0]),np.arange(self.arr.shape[1]))
        x = X[arr=="^"][0]
        y = Y[arr=="^"][0]
        self.curr_loc = np.array([y,x])
        self.arr[y,x] = '.'
        self.path = [(tuple(self.curr_loc),tuple(self.direction))]
        self.termstate = None

    def turn_right(self):
        self.direction =np.array([self.direction[1],-self.direction[0]])

    def step(self) -> bool:
        next_loc = self.curr_loc + self.direction
        if self.is_outside(next_loc):
            self.curr_loc = next_loc
            self.termstate = "outside"
            return False
        
        next_val = self.arr[next_loc[0],next_loc[1]]
        if next_val == "#":
            self.turn_right()
            return True
        
        if (tuple(next_loc),tuple(self.direction)) in self.path:
            self.curr_loc = next_loc
            self.termstate = "loop"
            return False
        
        self.curr_loc = next_loc
        self.path.append((tuple(self.curr_loc),tuple(self.direction)))
        return True
    
    def run(self):
        while self.step():
            pass 

    def is_outside(self,loc):
        if loc[0] < 0 or loc[0] >= self.arr.shape[0] or loc[1] < 0 or loc[1] >= self.arr.shape[1]:
            return True
        return False
    
    def unique_squares(self):
        return set([x[0] for x in self.path])
    
    def is_loop(self):
        return self.termstate == "loop"

with open("inputs/day6.txt") as f:
    arr = np.array([ [ c for c in l.strip()] for l in f],dtype=str)
print(arr.shape)

m = Map(arr.copy())
m.run()
print("default_path: ",len(m.unique_squares()))


#there's definately an optimization here, but we're early enough that
#we can brute force it
potential_obstacles = []
for p in tqdm(m.unique_squares()):
    a = arr.copy()
    i,j = p
    if a[i,j] != ".":
        continue
    a[i,j] = "#"
    m = Map(a)
    m.run()
    if m.is_loop():
        potential_obstacles.append((i,j))

print("obstacle locations: ",len(potential_obstacles))

