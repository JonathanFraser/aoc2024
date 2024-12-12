import numpy as np
from collections import defaultdict

with open("inputs/day12.txt") as f:
     arr = np.array([ [ c for c in l.strip()] for l in f],dtype=str)


seen = set()
regions = []
def process_region(i,j,value):
    
    if arr[i,j] != value:
        return (0,[])
    
    if (i,j) in seen:
        return (0,[])
    
    seen.add((i,j))

    up = (i,j-1)
    down = (i,j+1)
    left = (i-1,j)
    right = (i+1,j)
    dirs = [up,down,left,right]
    area_total = 1
    perimeters = []
    for d in dirs:
        if d[0] < 0 or d[0] >= arr.shape[0] or d[1] < 0 or d[1] >= arr.shape[1]:
            perimeters.append(((d[0],i), (d[1],j)))
            continue

        (a,p) = process_region(d[0],d[1],value)
        area_total += a
        perimeters += p
        if arr[d[0],d[1]] != value:
            perimeters.append(((d[0],i), (d[1],j)))

    return (area_total, perimeters)

for i in range(0,arr.shape[0]):
     for j in range(0,arr.shape[1]):
            if (i,j) in seen: 
                continue
            value = arr[i,j]
            regions.append(process_region(i,j,value))


def count_sides(perimeters):
    
    horizontals = defaultdict(list)
    verticals = defaultdict(list)

    for ((i1,i2),(j1,j2)) in perimeters:
        #j is x 
        #i is y
        if i1 != i2: #horizontal
            horizontals[(i1,i2)].append(j1)

        if j1 != j2:
            verticals[(j1,j2)].append(i1)

    sides = 0 
    for _,v in horizontals.items():
        values = set(v)
        for i in range(min(values),max(values)+1):
            if i in values and (i-1 not in values or i == min(values)):
                sides += 1

    for _,v in verticals.items():
        values = set(v)
        for i in range(min(values),max(values)+1):
            if i in values and (i-1 not in values or i == min(values)):
                sides += 1
 
    return sides

print(sum([r[0]*len(r[1]) for r in regions]))
print(sum([r[0]*count_sides(r[1]) for r in regions]))
