

import scipy.sparse as sp 

num_keys = ['0', '1', '2', '3', '4', '5', '6', '7' ,'8','9','A']
dir_keys = ["<",">","^","v","A"]

dir_keys_direction = {
    ("^",">") : "A",
    ("^", "v") : "v",
    ("<", ">") : "v",
    ("v", ">") : ">",
    ("v", "<") : "<", 
    ("v", "^") : "^", 
    (">", "^") : "A", 
    (">", "<") : "v", 
    ("A", "<") : "^", 
    ("A", "v") : ">"
}

num_keys_direction = {
    ("0","^") : "2",
    ("0",">") : "A",
    ("A", "<"): "0",
    ("A", "^"): "3", 
    ("1", "^"):"4",
    ("1", ">"): "2", 
    ("2", "^"):"5",
    ("2", ">"): "3",
    ("2", "<"): "1",
    ("2", "v"): "0",
    ("3", "^"):"6",
    ("3", "<"): "2",
    ("3", "v"): "A",
    ("4", "^"):"7",
    ("4", ">"): "5",
    ("4", "v"): "2",
    ("5", "^"):"8",
    ("5", ">"): "6",
    ("5", "<"): "4",
    ("5", "v"): "2",
    ("6", "^"):"9",
    ("6", "<"): "5",
    ("6", "v"): "3",
    ("7", ">"): "8",
    ("7", "v"): "4",
    ("8", ">"): "9",
    ("8", "<"): "7",
    ("8", "v"): "5",
    ("9", "<"): "8",
    ("9", "v"): "6"
}

def strings(): 
    for n in range(0,1000):
        t = str(n).zfill(3) + "A"
        for i in range(1,5):
            yield t[:i]

    yield ""

n = []
back_scatter = {}
for pad2 in dir_keys:
    for pad3 in dir_keys:
        for pad4 in num_keys: 
            for s in strings():
                back_scatter[(pad2,pad3,pad4,s)] = len(n)
                n.append((pad2,pad3,pad4,s))

mat = sp.lil_matrix((len(n),len(n)),dtype=int)
for (pad2,pad3,pad4,s) in n: 
    i = back_scatter[(pad2,pad3,pad4,s)]
    for user_pad_entry in ["<",">","^","v"]:
        if (pad2,user_pad_entry) not in dir_keys_direction:
            continue

        new_pad2 = dir_keys_direction[(pad2,user_pad_entry)]
        j = back_scatter[(new_pad2,pad3,pad4,s)]
        mat[i,j] = 1

    #for user pad entry A 
    if pad2 != "A":
        if (pad3,pad2) not in dir_keys_direction:
            continue

        new_pad3 = dir_keys_direction[(pad3,pad2)]
        j = back_scatter[(pad2,new_pad3,pad4,s)]
        mat[i,j] = 1
        continue

    if pad3 != "A":
        if (pad4,pad3) not in num_keys_direction:
            continue

        new_pad4 = num_keys_direction[(pad4,pad3)]
        j = back_scatter[(pad2,pad3,new_pad4,s)]
        
        mat[i,j] = 1
        continue

    new_code = s+pad4
    if (pad2,pad3,pad4,new_code) not in back_scatter:
        continue

    j = back_scatter[(pad2,pad3,pad4,new_code)]
    mat[i,j] = 1


start_pt = ("A","A","A","")
startn = back_scatter[start_pt]

dists,pred,sources = sp.csgraph.dijkstra(mat,indices=startn,min_only=True,return_predecessors=True)

complexity = 0 
with open("inputs/day21_test1.txt") as f:
    for l in f:
        input = l.strip()
        endn = back_scatter[("A","A","A",input)]
        distn = round(dists[endn])
        valuen = int(input[:-1])
        print(input,distn,valuen)
        complexity += distn*valuen


print(complexity)


                
