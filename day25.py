import numpy as np 
def read_grid(f):
    grid = []
    for l in f:
        lp = l.strip()
        if lp == "": 
            break
        grid.append(list(lp))
    
    if len(grid) == 0:
        return None
    
    return np.array(grid)

def process_grid(grid):
    islock = np.all(grid[0,:] == "#")
    iskey = np.all(grid[-1,:] == "#")
    if islock and iskey:
        raise ValueError("Invalid grid")
    
    gs = np.where(grid == "#",1,0)
    return (islock, np.sum(gs,axis=0)-1)

potentials = []
with open("inputs/day25.txt") as f:
    while True:
        g = read_grid(f)
        if g is None:
            break
        potentials.append(process_grid(g))


keys = np.array([k[1] for k in potentials if not k[0]])
locks = np.array([k[1] for k in potentials if k[0]])

count = 0
for k in keys:
    for l in locks: 
        if np.max(k+l) <= 5:
            count += 1

print(count)




