import re 
import numpy as np
from typing import Generator, Tuple, List

m = re.compile("XMAS")

def get_forward_diagonals(s: np.ndarray) -> Generator[str,None,None]:
    diagonals = [s[::-1,:].diagonal(i) for i in range(-s.shape[0]+1,s.shape[1])]
    for d in diagonals:
        yield "".join(d)

def get_backward_diagonals(s: np.ndarray) -> Generator[str,None,None]:
    diagonals = [s.diagonal(i) for i in range(s.shape[1]-1,-s.shape[0],-1)]
    for d in diagonals:
        yield "".join(d)


grid = []
with open('inputs/day4.txt') as f:
    grid = list([list(l.rstrip()) for l in f])


s = np.array(grid)
print("shape: ", s.shape)


count = 0
for i in s:
    j = "".join(i)
    count += len(m.findall(j[:])) #forwards
    count += len(m.findall(j[::-1])) #backwards

for i in s.transpose():
    j = "".join(i)
    count += len(m.findall(j[:])) #forwards
    count += len(m.findall(j[::-1])) #backwards

for i in get_forward_diagonals(s):
    count += len(m.findall(i[:])) #forwards
    count += len(m.findall(i[::-1])) #backwards

for i in get_backward_diagonals(s):
    count += len(m.findall(i[:])) #forwards
    count += len(m.findall(i[::-1])) #backwards

print(count)

def isMas(s: list[str]) -> bool:
    t = "".join(s)
    return t == "MAS" or t == "SAM"

def isXMas(g: np.ndarray, A_loc : Tuple[int,int]) -> bool:
    (i,j) = A_loc
    
    #can't form an X if the A is on the edge
    if i == 0 or i == g.shape[0] - 1:
        return 0 
    
    if j == 0 or j == g.shape[1] - 1:
        return 0
    
    diag1 = [g[i-1][j-1], g[i][j], g[i+1][j+1]]
    diag2 = [g[i-1][j+1], g[i][j], g[i+1][j-1]]



    if isMas(diag1) and isMas(diag2):
        return 1



x_count = 0 
for i in range(0, s.shape[0]):
    for j in range(0, s.shape[1]):
        if s[i][j] == "A":
            x_count += isXMas(s, (i,j))


print(x_count)