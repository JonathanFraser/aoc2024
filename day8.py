import numpy as np

with open("inputs/day8.txt") as f:
    arr = np.array([ [ c for c in l.strip()] for l in f],dtype=str)

frequencies = set(arr.flatten())
frequencies.remove('.')
Nmax = len(np.diag(arr))**2
X,Y = np.meshgrid(np.arange(arr.shape[0]),np.arange(arr.shape[1]))

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

            # l2 - (l1 - l2) so delta from l2 to l1 and then backwards from l2
            antinode = (loc2[0] - loc1[0] + loc2[0], loc2[1] - loc1[1] + loc2[1])
            if antinode[0] < 0 or antinode[0] >= arr.shape[0] or antinode[1] < 0 or antinode[1] >= arr.shape[1]:
                continue
            antinodes_x2.add(antinode)

            (dx,dy) = (loc2[0]-loc1[0],loc2[1]-loc1[1])

            stp = np.gcd.reduce([dx,dy])
            if stp != 0:
                (dx,dy) = (dx//stp,dy//stp)
            
            for i in range(0,Nmax):
                l3x = i*dx+loc2[0]
                l3y = i*dy+loc2[1]
                if l3x >= arr.shape[0] or l3y >= arr.shape[1] or l3x < 0 or l3y < 0:
                    break
                antinodes_all.add((l3x,l3y))

            for i in range(0,-Nmax,-1):
                l3x = i*dx+loc2[0]
                l3y = i*dy+loc2[1]
                if l3x >= arr.shape[0] or l3y >= arr.shape[1] or l3x < 0 or l3y < 0:
                    break
                antinodes_all.add((l3x,l3y))


print(len(antinodes_x2))
print(len(antinodes_all))

   
