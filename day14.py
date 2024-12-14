import re 
import sys
import numpy as np 
np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)
r = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

bots = []

grid_size = np.array((101,103))
#grid_size = np.array((11,7))
with open('inputs/day14.txt') as f:
    for l in f:
        m = r.match(l)
        (px,py,vx,vy) = m.groups()
        bots.append((np.array([int(px),int(py)],dtype=int),np.array([int(vx),int(vy)],dtype=int)))


sector_count = np.array([0,0,0,0])
seconds = 100
for b in bots:
    (bp,bv) = b
    bf = (bp + bv*seconds) % grid_size
    if bf[0] == (grid_size[0]-1)//2 or bf[1] == (grid_size[1]-1)//2:
        continue 

    idx = 0 
    if bf[0] > (grid_size[0]-1)//2:
        idx += 1 

    if bf[1] > (grid_size[1]-1)//2:
        idx += 2

    sector_count[idx] += 1
print(sector_count.prod())


# Part 2
for s in range(0,101*103):
    arr = np.zeros((grid_size[0],grid_size[1]),dtype=str)
    arr[:,:] = "."
    for b in bots:
        (bp,bv) = b
        bf = (bp + bv*s) % grid_size
        arr[bf[0],bf[1]] = "*"
    
    for a in arr:
        l = "".join(a)
        if "**********" in l:
            print(s)
