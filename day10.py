import numpy as np

with open('inputs/day10.txt') as f:
    arr = np.array([ [ int(c) for c in l.strip()] for l in f])

[Y,X] = np.meshgrid(np.arange(0,arr.shape[0]),np.arange(0,arr.shape[1]))

peaks_x = X[arr == 9]
peaks_y = Y[arr == 9]

peaks = list(zip(peaks_x,peaks_y))

trail_head_x = X[arr == 0]
trail_head_y = Y[arr == 0]
trail_heads = list(zip(trail_head_x,trail_head_y))

seen = {}
routes = {}
for p in peaks:
    seen[p] = set([p])
    routes[p] = 1

def is_outside(loc):
    if loc[0] < 0 or loc[0] >= arr.shape[0] or loc[1] < 0 or loc[1] >= arr.shape[1]:
        return True
    return False

def get_accessible(loc,level=0):
    if is_outside(loc):
        return (set(),0)
    
    if arr[loc] != level:
        return (set(),0)
    
    if loc in seen:
        return (seen[loc],routes[loc])
    
    up = (loc[0],loc[1]-1)
    down = (loc[0],loc[1]+1)
    left = (loc[0]-1,loc[1])
    right = (loc[0]+1,loc[1])

    dirs = [up,down,left,right]
    accessible = set()
    route_count = 0
    for d in dirs:
        acc,rc = get_accessible(d,level+1)
        accessible = accessible.union(acc)
        route_count += rc 

    seen[loc] = accessible
    routes[loc] = route_count
    
    return (accessible,route_count)

sum = 0 
route_sum = 0
for th in trail_heads:
    accessible,rc = get_accessible(th)
    print(th,len(accessible),rc)
    sum += len(accessible)
    route_sum += rc
    print()


print(sum)
print(route_sum)