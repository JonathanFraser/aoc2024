import os 

with open("inputs/day1.txt") as file:
    left = []
    right = []
    for line in file:
        ls = line.split(' ')
        l = ls[0]
        r = ls[-1]
        left.append(int(l))
        right.append(int(r))

    lsr = left.sort()
    rsr = right.sort()

    total = 0
    for (l,r) in zip(left,right):
        total  += abs(l-r)

    print("distance: ", total)

    counts = {}
    for r in right:
        counts[r] = counts.get(r,0)+1
    
    total = 0
    for l in left: 
        total += counts.get(l,0)*l

    print("similarity: ", total)
