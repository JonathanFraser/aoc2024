
import numpy as np 
from collections import defaultdict

def mix(n: int, m: int):
    return n ^ m

def prune(n: int):
    return n % 16777216

def evolve_next_secret(n: int):
    n2 = prune(mix(n*64,n))
    n3 = prune(mix(n2 // 32 ,n2))
    return prune(mix(n3*2048,n3))

evolve_vec = np.vectorize(evolve_next_secret)

secrets = []
with open('inputs/day22.txt') as f:
    for l in f:
        s = int(l.strip())
        secrets.append(s)

arr = np.zeros((len(secrets),2001),dtype=int)
arr[:,0] = secrets
for i in range(1,2001):
    arr[:,i] = evolve_vec(arr[:,i-1])

print(arr[:,-1].sum())

deltas = np.diff(arr % 10,axis=1)
print(deltas.shape)

value_maps = [0] * len(secrets)

for c in range(0,len(secrets)):
    value_map = {}
    for i in range(3,deltas.shape[1]):
        key = tuple(deltas[c,i-3:i+1])
        if key not in value_map:
            value = arr[c,i+1]
            value_map[key] = value % 10

    value_maps[c] = value_map

dict = defaultdict(int)
for (i,map) in enumerate(value_maps):
    for k,v in map.items():
        dict[k] += v

max_key = max(dict,key=dict.get)
print(max_key)
print(dict[max_key])