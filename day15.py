import numpy as np 

with open('inputs/day15.txt') as f:
    arr = []
    for l in f:
        if l.strip() == "":
            break
        arr.append([c for c in l.strip()])

    arr = np.array(arr,dtype=str)


    moves = ""
    for l in f:
        moves += l.strip()

X,Y = np.meshgrid(np.arange(arr.shape[1]),np.arange(arr.shape[0]))

wall_x = X[arr == "#"]
wall_y = Y[arr == "#"]
bot_x = X[arr == "@"]
bot_y = Y[arr == "@"]
box_x = X[arr == "O"]
box_y = Y[arr == "O"]
walls = set(zip(wall_x,wall_y))
boxes = set(zip(box_x,box_y))
bot = (bot_x[0],bot_y[0])

def ptr_right(loc):
    (x,y) = loc
    return (x+1,y)

def ptr_left(loc):
    (x,y) = loc
    return (x-1,y)

def ptr_up(loc):
    (x,y) = loc
    return (x,y-1)

def ptr_down(loc):
    (x,y) = loc
    return (x,y+1)

dir = {
    "<": ptr_left,
    ">": ptr_right,
    "^": ptr_up,
    "v": ptr_down
}

def move_box(loc,d):
    next_pt = dir[d](loc)
    if next_pt in walls:
        return False
    
    if next_pt in boxes:
        r = move_box(next_pt,d)
        if not r: 
            return False
        
    boxes.remove(loc)
    boxes.add(next_pt)
    return True
        
    
        
def move_bot(loc,d):
    global bot
    next_pt = dir[d](loc)
    if next_pt in walls:
        return False
    
    if next_pt in boxes:
        r = move_box(next_pt,d)
        if not r:
            return False

    bot = next_pt
    return True


for m in moves:
    move_bot(bot,m)

gps_total = 0
for (x,y) in boxes:
    gps_total += 100*y + x 

print(gps_total)

def expand(v):
    if v == "#":
        return "##"
    if v == "@":
        return "@."
    if v == "O":
        return "[]"
    if v == ".":
        return ".."

arr2 = np.vectorize(expand)(arr)
arr3 = np.zeros((arr2.shape[1],2*arr2.shape[0]),dtype=str)

for i in range(0,arr2.shape[0]):
    arr3[i] = list("".join(arr2[i]))

print(arr3)

X2,Y2 = np.meshgrid(np.arange(arr3.shape[1]),np.arange(arr3.shape[0]))

wall_x2 = X2[arr3 == "#"]
wall_y2 = Y2[arr3 == "#"]
box_x2 = X2[arr3 == "["]
box_y2 = Y2[arr3 == "["]
box_x2_r = X2[arr3 == "]"]
box_y2_r = Y2[arr3 == "]"]
bot_x2 = X2[arr3 == "@"]
bot_y2 = Y2[arr3 == "@"]

walls2 = set(zip(wall_x2,wall_y2))
boxes2 = set(zip(box_x2,box_y2))
boxes2_r = set(zip(box_x2_r,box_y2_r))
bot2 = (bot_x2[0],bot_y2[0])

def move_box2(loc,d,move_set=set()):
    next_pt = dir[d](loc)
    next_r_pt = dir[d](ptr_right(loc))
    move_set.add(loc)
    move_set.add(ptr_right(loc))

    if next_pt in walls2 or next_r_pt in walls2:
        return False
    
    if next_pt in boxes2 and next_pt not in move_set:
        r = move_box2(next_pt,d,move_set)
        if not r:
            return False
        
    if next_r_pt in boxes2 and next_r_pt not in move_set:
        r = move_box2(next_r_pt,d,move_set)
        if not r:
            return False
        
    if next_pt in boxes2_r and next_pt not in move_set:
        r = move_box2(ptr_left(next_pt),d,move_set)
        if not r:
            return False
        
    if next_r_pt in boxes2_r and next_r_pt not in move_set:
        r = move_box2(ptr_left(next_r_pt),d,move_set)
        if not r:
            return False

    return True


def move_bot2(d):
    global bot2
    next_pt = dir[d](bot2)
    if next_pt in walls2:
        #print("failed to move: ",d,(bot2,next_pt), "wall")
        return False
    
    moves = set()
    if next_pt in boxes2:
        r = move_box2(next_pt,d,moves)
        if not r:
            #print("failed to move: ",d,(bot2,next_pt), "box_block")
            return False
    
    if next_pt in boxes2_r:
        r = move_box2(ptr_left(next_pt),d,moves)
        if not r:
            #print("failed to move: ",d,(bot2,next_pt), "box_r_block")
            return False
        
    def box2_add(n):
        return lambda: boxes2.add(n)
    
    def box2_r_add(n):
        return lambda: boxes2_r.add(n)
        
    
    defer = []
    for m in moves:
        n = dir[d](m)
        if m in boxes2:
            boxes2.remove(m)
            defer.append(box2_add(n))
        if m in boxes2_r:
            boxes2_r.remove(m)
            defer.append(box2_r_add(n))

    for df in defer:
        df()

    #print("move: ",d,(bot2,next_pt))

    bot2 = next_pt
    return True
    

for m in moves:
    move_bot2(m)

arr4 = np.zeros(arr3.shape,dtype=str)
arr4[:,:] = "."
for w in walls2:
    arr4[w[1],w[0]] = "#"

sum_long = 0 
for b in boxes2:
    sum_long += 100*b[1] + b[0]
    arr4[b[1],b[0]] = "["

for b in boxes2_r:
    arr4[b[1],b[0]] = "]"

arr4[bot2[1],bot2[0]] = "@"

print(sum_long)
