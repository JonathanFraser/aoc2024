from helper import Point 
from typing import Dict 
from itertools import permutations

class KeyPad():
    a_pos : Point = None 
    keys : Dict[str,Point] = {}
    blacklist :Point=None

    def __init__(self):
        pass

    def set_home(self):
        self.a_pos = self.keys["A"]

    def get_paths(self,start,end):
        target_loc : Point = self.keys[end]
        start_pos : Point = self.keys[start] 

        xdelta = target_loc.x - start_pos.x
        ydelta = target_loc.y - start_pos.y 

        moves = ""
        if xdelta > 0:
            moves += ">"*abs(xdelta)
        else: 
            moves += "<"*abs(xdelta)

        if ydelta > 0: 
            moves += "v"*abs(ydelta)
        else:
            moves += "^"*abs(ydelta)

        seen = set()
        for p in permutations(moves):
            mstr = "".join(p)
            if mstr in seen:
                continue 
            seen.add(mstr)
            curr_loc = start_pos
            for m in p:
                curr_loc = curr_loc.move(m)
                if curr_loc == self.blacklist:
                    break
            if curr_loc != target_loc:
                continue 

            yield mstr+"A"

class NumPad(KeyPad):
    def __init__(self):
        super(KeyPad).__init__()
        self.keys = {
            "0": Point(1,3),
            "1": Point(0,2),
            "2": Point(1,2),
            "3": Point(2,2),
            "4": Point(0,1),
            "5": Point(1,1),
            "6": Point(2,1),
            "7": Point(0,0),
            "8": Point(1,0),
            "9": Point(2,0),
            "A": Point(2,3)
        }
        self.blacklist = Point(0,3)
        self.set_home()

class DirPad(KeyPad):
    def __init__(self):
        super(KeyPad).__init__()
        self.keys = {
            ">": Point(2,1),
            "<": Point(0,1),
            "v": Point(1,1),
            "^": Point(1,0),
            "A": Point(2,0)
        }
        self.blacklist = Point(0,0)
        self.set_home()


def get_shortest_seq(sequence,depth=0,cache = {}):
    d = DirPad()
 
    if depth == 0:
        return len(sequence)
    
    if (sequence,depth) in cache:
        return cache[(sequence,depth)]

    retval = 0
    for (f,t) in zip("A"+sequence,sequence):
        min_len = float("inf")
        for path in d.get_paths(f,t):
            seq_len = get_shortest_seq(path,depth-1)
            if seq_len < min_len:
                min_len = seq_len
        retval += min_len
    cache[(sequence,depth)] = retval
    return retval

def  get_input_code(sequence,depth=0,cache = {}):
    n = NumPad()
    retval = 0
    for (f,t) in zip("A"+sequence,sequence):
        min_len = float("inf")
        for p in n.get_paths(f,t):
            seq_len = get_shortest_seq(p,depth=depth,cache=cache)
            if seq_len < min_len:
                min_len = seq_len
        retval += min_len
    
    return retval
    
complexity = 0 
complexity2 = 0 
with open('inputs/day21.txt') as f:
    for l in f:
        k = l.strip()
        cache = {}
        num = int(k[:-1])
        min_seq = get_input_code(k,depth=2,cache=cache)
        min_seq2 = get_input_code(k,depth=25,cache=cache)
        complexity += num*min_seq
        complexity2 += num*min_seq2

print(complexity)
print(complexity2)