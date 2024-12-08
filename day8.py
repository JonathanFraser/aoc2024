import numpy as np

with open("inputs/day8.txt") as f:
    arr = np.array([ [ c for c in l.strip()] for l in f],dtype=str)

frequencies = set(arr.flatten())
frequencies.remove('.')
Nmax = len(np.diag(arr))**2
X,Y = np.meshgrid(np.arange(arr.shape[0]),np.arange(arr.shape[1]))

def is_outside(loc):
    if loc[0] < 0 or loc[0] >= arr.shape[0] or loc[1] < 0 or loc[1] >= arr.shape[1]:
        return True
    return False

antinodes_x2 = set()
antinodes_all = set()
for f in frequencies:
    Xs = X[arr==f]
    Ys = Y[arr==f]
    flocs = list(zip(Xs.flatten(),Ys.flatten()))
    for loc1 in flocs:
        for loc2 in flocs:
            if loc1 == loc2:
                continue

            l1 = np.array(list(loc1))
            l2 = np.array(list(loc2))
            delta = l1 - l2
            antinode = l2 - delta

            if is_outside(antinode):
                continue
            antinodes_x2.add(tuple(antinode))

            stp = np.gcd.reduce(delta)
            if stp != 0:
                delta = delta//stp
            
            for i in range(0,Nmax):
                l3 = l2 + i*delta
                if not is_outside(l3):
                    antinodes_all.add(tuple(l3))
                
                l3n = l2 - i*delta
                if not is_outside(l3n):
                    antinodes_all.add(tuple(l3n))

                if is_outside(l3) and is_outside(l3n):
                    break

print(len(antinodes_x2))
print(len(antinodes_all))

   
