
import re
import numpy as np 

but_match = re.compile(r"Button ([AB]): X\+(\d+), Y\+(\d+)")
prize_match = re.compile(r"Prize: X=(\d+), Y=(\d+)")

with open("inputs/day13.txt") as f:
    values = []
    val = {}
    for l in f:
        if l.strip() == "":
            values.append(val)
            val = {}
            continue
        m = but_match.match(l)
        if m:
            val[m.group(1)] = np.array([int(m.group(2)),int(m.group(3))],dtype=int)
            continue
        m = prize_match.match(l)
        if m:
            val["prize"] = np.array([int(m.group(1)),int(m.group(2))],dtype=int)
            continue
values.append(val)

weights = np.array([3,1],dtype=int)
def compute_cost(ainc,binc,prize):


    M = np.matrix([ainc,binc]).T 
    if np.linalg.matrix_rank(M) < 2:
        print("EXPLOSION")
        print(M)
        quit()

    presses = np.linalg.solve(M,prize)
    if np.any(presses < 0):
        return (None,0)

    press_int = np.round(presses).astype(dtype=int)
    match = np.all(M@press_int == prize)
    if match:
        return (press_int,3*press_int[0]+press_int[1])

    return (None,0)



min_cost = 0 
farther_cost = 0 
for v in values:
    (solution,cost) = compute_cost(v["A"],v["B"],v["prize"])
    if solution is not None: 
        min_cost += cost

    (solution,cost) = compute_cost(v["A"],v["B"],v["prize"]+np.array([10000000000000,10000000000000]))
    if solution is not None:
        farther_cost += cost

print(min_cost)
print(farther_cost)