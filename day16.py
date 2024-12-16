import numpy as np
import scipy.sparse as sp


with open("inputs/day16.txt") as f:
    arr = np.array([ [ c for c in l.strip()] for l in f],dtype=str)

nodes = []
start = None
end = None

for y in range(0,arr.shape[0]):
    for x in range(0,arr.shape[1]):
        if arr[y,x] == "#":
            continue

        if arr[y,x] == "S":
            start = (x,y)
        
        if arr[y,x] == "E":
            end = (x,y)

        nodes.append((x,y,"^"))
        nodes.append((x,y,"v"))
        nodes.append((x,y,"<"))
        nodes.append((x,y,">"))


options = [[] for _ in nodes]

nodemap = {n:i for (i,n) in enumerate(nodes)}


for (i,n) in enumerate(nodes):
    (x,y,d) = n
    if d == "^":
        options[i].append((i+2,1000))
        options[i].append((i+3,1000))
        if (x,y-1,"^") in nodemap:
            options[i].append((nodemap[(x,y-1,"^")],1))

    if d == "v":
        options[i].append((i+1,1000))
        options[i].append((i+2,1000))
        if (x,y+1,"v") in nodemap:
            options[i].append((nodemap[(x,y+1,"v")],1))

    
    if d == "<": 
        options[i].append((i-1,1000))
        options[i].append((i-2,1000))
        if (x-1,y,"<") in nodemap:
            options[i].append((nodemap[(x-1,y,"<")],1))
        
    if d == ">":
        options[i].append((i-2,1000))
        options[i].append((i-3,1000))
        if (x+1,y,">") in nodemap:
            options[i].append((nodemap[(x+1,y,">")],1))


mat = sp.lil_matrix((len(nodes),len(nodes)),dtype=int)
for (i,o) in enumerate(options):
    for (n,cost) in o:
        mat[i,n] = cost
startn = nodemap[(start[0],start[1],">")]
endn = [nodemap[n] for n in [(end[0],end[1],"<"),(end[0],end[1],">"),(end[0],end[1],"^"),(end[0],end[1],"v")]]
(dist,pred,sources) = sp.csgraph.dijkstra(mat,indices=startn,return_predecessors=True,directed=True,min_only=True)
mindist = int(dist[endn].min())
print(mindist)

costs = [(None,[]) for _ in range(0,len(nodes))]
seen = set()
to_process = [startn]
costs[startn] = (0,[[startn]])

while len(to_process) > 0:
    n = to_process.pop(0)
    (curr_cost,prev_paths) = costs[n]
    if (n,curr_cost) in seen:
        continue
    seen.add((n,curr_cost))

    
    for (next_node,leg_cost) in options[n]:
        to_process.append(next_node)

        (next_cost,next_paths) = costs[next_node]
        if curr_cost + leg_cost == next_cost:
            costs[next_node] = (next_cost,next_paths + [p+[next_node] for p in prev_paths])
            
        if next_cost is None or curr_cost + leg_cost < next_cost :
            costs[next_node] = (curr_cost + leg_cost,[p+[next_node] for p in prev_paths])


touched = set()
for e in endn:
    (c,paths) = costs[e]
    if c == mindist:
        for p in paths:
            touched.update(p)

print(len(set([nodes[t][:2] for t in touched])))





